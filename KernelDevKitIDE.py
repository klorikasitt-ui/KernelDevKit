import os
import subprocess
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DirectoryTree, RichLog, TextArea, Button
from textual.containers import Horizontal, Vertical, Container

class KernelDevKitIDE(App):
    """Kod Editörü, Dosya Yöneticisi ve 20+ Dil Destekli Akıllı Derleyici"""
    
    # CSS'deki border hataları düzeltildi
    CSS = """
    #main-layout { layout: horizontal; }
    #left-panel { width: 25%; border-right: heavy cyan; background: #121212; }
    #right-panel { width: 75%; }
    
    /* Hata veren 'thin' yerine 'solid' kullanıldı */
    #editor { height: 65%; border-bottom: solid gray; } 
    #log-panel { height: 35%; background: #000000; }
    
    #button-bar { height: 3; background: #1a1a1a; align: center middle; border-bottom: solid cyan; }
    Button { margin: 0 1; min-width: 20; }
    """

    BINDINGS = [
        ("ctrl+s", "save_file", "Kaydet"),
        ("ctrl+r", "compile_run", "Derle/Çalıştır"),
        ("q", "quit", "Çıkış")
    ]

    def __init__(self):
        super().__init__()
        self.current_file = None
        # Genişletilmiş Derleyici Listesi
        self.compilers = {
            ".c": ("gcc", "-Wall -o"),
            ".cpp": ("g++", "-Wall -o"),
            ".asm": ("nasm", "-f elf32 -o"),
            ".py": ("python", ""),
            ".rs": ("rustc", "-O"),
            ".js": ("node", ""),
            ".go": ("go build", ""),
            ".java": ("javac", ""),
            ".sh": ("bash", ""),
            ".lua": ("lua", "")
        }

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main-layout"):
            # Dosya Yöneticisi
            yield DirectoryTree("./", id="left-panel")
            
            with Vertical(id="right-panel"):
                # Üst Buton Barı
                with Horizontal(id="button-bar"):
                    yield Button("💾 KAYDET", id="save_btn", variant="success")
                    yield Button("🚀 DERLE & ÇALIŞTIR", id="run_btn", variant="primary")
                
                # Editör ve Log Alanı
                yield TextArea(id="editor", language="python", theme="monokai")
                yield RichLog(id="log-panel", markup=True, highlight=True)
        yield Footer()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Seçilen dosyayı editöre yükler."""
        self.current_file = str(event.path)
        try:
            with open(self.current_file, "r", encoding="utf-8") as f:
                content = f.read()
                editor = self.query_one("#editor", TextArea)
                editor.load_text(content)
                
                # Uzantıya göre sözdizimi renklendirme
                _, ext = os.path.splitext(self.current_file)
                ext_map = {".py": "python", ".c": "c", ".cpp": "cpp", ".js": "javascript", ".json": "json"}
                editor.language = ext_map.get(ext, "python")
                
                self.log_message(f"[bold cyan]Açıldı:[/] {self.current_file}")
        except Exception as e:
            self.log_message(f"[bold red]Hata:[/] {e}")

    def log_message(self, message: str):
        self.query_one("#log-panel", RichLog).write(message)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            self.action_save_file()
        elif event.button.id == "run_btn":
            self.action_compile_run()

    def action_save_file(self):
        if self.current_file:
            content = self.query_one("#editor", TextArea).text
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(content)
                self.log_message("[bold green]✔ Kaydedildi![/]")
            except Exception as e:
                self.log_message(f"[bold red]Kayıt Hatası:[/] {e}")
        else:
            self.log_message("[bold red]Önce bir dosya seçin![/]")

    def action_compile_run(self):
        if not self.current_file:
            return
        
        self.action_save_file()
        name, ext = os.path.splitext(self.current_file)
        
        if ext not in self.compilers:
            self.log_message(f"[bold red]Desteklenmeyen uzantı:[/] {ext}")
            return

        cmd, flags = self.compilers[ext]
        out_name = name if ext not in [".py", ".js", ".sh", ".lua"] else ""
        full_cmd = f"{cmd} {self.current_file} {flags} {out_name}".strip()
        
        self.log_message(f"[bold yellow]⚙ İşlem:[/] {full_cmd}")
        
        try:
            process = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
            if process.returncode == 0:
                self.log_message("[bold green]✔ Başarılı![/]")
                if process.stdout:
                    self.log_message(f"[white]{process.stdout}[/]")
            else:
                self.log_message(f"[bold red]❌ HATA ÇIKTISI:[/]\n{process.stderr}")
        except Exception as e:
            self.log_message(f"[bold red]Sistem Hatası:[/] {e}")

if __name__ == "__main__":
    KernelDevKitIDE().run()
  
