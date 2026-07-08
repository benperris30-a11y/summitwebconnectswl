import json
import os
import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.utils import platform

# Hook into native Android elements
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
   
    # Isolate the webview data directory immediately for clean Android runtime stability
    try:
        WebView.setDataDirectorySuffix("summit_webview_isolated")
    except Exception as e:
        print(f"Directory suffix already set or skipped: {e}")
else:
    def run_on_ui_thread(func):
        return func

# Brand colors
NAVY = get_color_from_hex("#0f2028")
NAVY_LIGHT = get_color_from_hex("#16303a")
TEAL = get_color_from_hex("#3fb8af")
TEXT_MUTED = get_color_from_hex("#9fb2b8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "summit_settings.json")

class SummitApp(App):
    def build(self):
        Window.clearcolor = NAVY
        self.settings = self._load_settings()
        self.selected_profile_index = None
        self.pending_url = ""
        self.native_webview = None
       
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
       
        self.main_layout.add_widget(Label(
            text="SoundWorks Lakes", color=TEAL, font_size='24sp', bold=True,
            size_hint_y=None, height='50dp'
        ))
        self.main_layout.add_widget(Label(
            text="Summit WebViewer", color=(1, 1, 1, 1), font_size='16sp',
            size_hint_y=None, height='30dp'
        ))

        self.list_scroll = ScrollView(size_hint=(1, 0.4))
        self.profile_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.profile_list_layout.bind(minimum_height=self.profile_list_layout.setter('height'))
        self.list_scroll.add_widget(self.profile_list_layout)
        self.main_layout.add_widget(self.list_scroll)

        self.input_area = BoxLayout(orientation='vertical', size_hint_y=None, height='200dp', spacing=5)
        self.name_input = TextInput(hint_text="Device Name", multiline=False, size_hint_y=None, height='40dp')
        self.ip_input = TextInput(hint_text="IP Address", multiline=False, size_hint_y=None, height='40dp')
       
        btn_row = BoxLayout(spacing=10, size_hint_y=None, height='50dp')
        save_btn = Button(text="Save", background_color=TEAL, on_press=self.save_profile)
        del_btn = Button(text="Delete", background_color=(0.7, 0.2, 0.2, 1), on_press=self.delete_profile)
        btn_row.add_widget(save_btn)
        btn_row.add_widget(del_btn)
       
        self.input_area.add_widget(Label(text="Profile Management", color=TEAL, size_hint_y=None, height='30dp'))
        self.input_area.add_widget(self.name_input)
        self.input_area.add_widget(self.ip_input)
        self.input_area.add_widget(btn_row)
        self.main_layout.add_widget(self.input_area)

        self.launch_btn = Button(
            text="Launch Selected Portal", background_color=TEAL,
            size_hint_y=None, height='60dp', on_press=self.launch_process
        )
        self.main_layout.add_widget(self.launch_btn)
       
        self.status_label = Label(text="Select a profile to begin", color=TEXT_MUTED, size_hint_y=None, height='30dp')
        self.main_layout.add_widget(self.status_label)

        self.refresh_profiles()
        return self.main_layout

    def _load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        return {"skip_disclaimer": False, "profiles": [{"name": "Default Streamer", "ip": "192.168.1.116"}]}

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            self.status_label.text = f"Save Error: {e}"

    def refresh_profiles(self):
        self.profile_list_layout.clear_widgets()
        for i, profile in enumerate(self.settings["profiles"]):
            btn = Button(text=f"{profile['name']} ({profile['ip']})", size_hint_y=None, height='50dp', background_color=NAVY_LIGHT, color=(1,1,1,1))
            btn.bind(on_press=lambda instance, idx=i: self.select_profile(idx))
            self.profile_list_layout.add_widget(btn)

    def select_profile(self, index):
        self.selected_profile_index = index
        profile = self.settings["profiles"][index]
        self.name_input.text = profile["name"]
        self.ip_input.text = profile["ip"]
        self.status_label.text = f"Selected: {profile['name']}"

    def save_profile(self, instance):
        name = self.name_input.text.strip()
        ip = self.ip_input.text.strip()
        if not name or not ip: return
        new_data = {"name": name, "ip": ip}
        if self.selected_profile_index is not None:
            self.settings["profiles"][self.selected_profile_index] = new_data
        else:
            self.settings["profiles"].append(new_data)
        self._save_settings()
        self.refresh_profiles()
        self.status_label.text = "Profile saved!"

    def delete_profile(self, instance):
        if self.selected_profile_index is None: return
        del self.settings["profiles"][self.selected_profile_index]
        self.selected_profile_index = None
        self._save_settings()
        self.refresh_profiles()
        self.name_input.text = ""
        self.ip_input.text = ""

    def launch_process(self, instance):
        host_input = self.ip_input.text.strip()
        if not host_input: return
        self.launch_btn.disabled = True
        self.status_label.text = "Checking connection..."
       
        if ":" in host_input:
            try:
                host, port_str = host_input.split(":", 1)
                ports = [int(port_str)]
            except:
                self.status_label.text = "Error: Invalid Port"
                self.launch_btn.disabled = False
                return
        else:
            host = host_input
            ports = [80, 9000, 9002]

        threading.Thread(target=self._network_worker, args=(host, ports), daemon=True).start()

    def _network_worker(self, host, ports):
        working_port = None
        for port in ports:
            try:
                url = f"http://{host}:{port}/"
                resp = requests.get(url, timeout=3)
                if resp.status_code == 200:
                    working_port = port
                    break
            except Exception as e:
                print(f"Port {port} check failed: {e}")
                continue

        if working_port:
            self.pending_url = f"http://{host}:{working_port}/"
        else:
            self.pending_url = f"http://{host}:{ports[0]}/"
           
        Clock.schedule_once(self.display_embedded_webpage, 0)

    def display_embedded_webpage(self, dt=None):
        self.launch_btn.disabled = False
        if platform == 'android':
            self._create_native_webview(self.pending_url)
        else:
            import webbrowser
            webbrowser.open(self.pending_url)

    @run_on_ui_thread
    def _create_native_webview(self, url):
        try:
            self.native_webview = WebView(activity)
            settings = self.native_webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setUseWideViewPort(True)
            settings.setLoadWithOverviewMode(True)
            
            # Instruct WebView to natively render standard HTTP/Mixed content streams
            try:
                settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
            except:
                pass

            self.native_webview.setWebViewClient(WebViewClient())
           
            layout_params = LayoutParams(int(-1), int(-1))
            activity.addContentView(self.native_webview, layout_params)
            self.native_webview.loadUrl(url)
        except Exception as e:
            print(f"Native WebView Crash: {e}")
            self.status_label.text = f"WebView Error: {e}"
            self.launch_btn.disabled = False

    def on_start(self):
        Window.bind(on_keyboard=self._handle_back_button)

    def _handle_back_button(self, window, key, *args):
        if key == 27: # Android Back Button
            if self.native_webview:
                self._close_webview()
                return True
        return False

    @run_on_ui_thread
    def _close_webview(self):
        if self.native_webview:
            try:
                parent = self.native_webview.getParent()
                if parent:
                    parent.removeView(self.native_webview)
                self.native_webview = None
                self.status_label.text = "Returned to Profile Selector."
            except Exception as e:
                print(f"Error closing: {e}")

if __name__ == "__main__":
    SummitApp().run()