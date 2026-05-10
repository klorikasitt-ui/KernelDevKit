# Değişkenler
PYTHON = python3
PIP = pip3
APP_NAME = KernelDevKitIDE.py
# Standart Linux sistemlerinde kullanıcı komutları buraya konur
INSTALL_DIR = /usr/local/bin
BIN_NAME = kdk

# Renkler
CYAN = \033[0;36m
GREEN = \033[0;32m
RED = \033[0;31m
RESET = \033[0m

.PHONY: help install uninstall run

help:
	@echo "$(CYAN)KernelDevKitIDE - Linux Kurulum Menüsü:$(RESET)"
	@echo "  sudo make install   - IDE'yi sistem genelinde (kdk) kurar"
	@echo "  sudo make uninstall - Sistemden kaldırır"
	@echo "  make run            - Kurulum yapmadan yerel olarak çalıştırır"

install:
	@echo "$(CYAN)📦 Kurulum Başlatılıyor...$(RESET)"
	@# Bağımlılıkların kurulu olduğundan emin ol
	@$(PIP) install textual --quiet || echo "$(RED)Hata: pip3 veya textual yüklenemedi!$(RESET)"
	@# Çalıştırılabilir script oluşturma
	@echo "#!/usr/bin/env $(PYTHON)" > $(BIN_NAME)
	@cat $(APP_NAME) >> $(BIN_NAME)
	@# İzinleri ayarla ve taşı (sudo yetkisi gerekebilir)
	@chmod +x $(BIN_NAME)
	@sudo mv $(BIN_NAME) $(INSTALL_DIR)/
	@echo "$(GREEN)✅ Başarıyla kuruldu! Terminale 'kdk' yazarak başlatabilirsiniz.$(RESET)"

uninstall:
	@sudo rm -f $(INSTALL_DIR)/$(BIN_NAME)
	@echo "$(GREEN)🗑️ Sistemden başarıyla kaldırıldı.$(RESET)"

run:
	$(PYTHON) $(APP_NAME)
