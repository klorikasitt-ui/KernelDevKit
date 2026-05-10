# Değişkenler
PYTHON = python3
PIP = pip
APP_NAME = KernelDevKitIDE.py
# Termux'un standart komut dizini
BIN_DIR = /data/data/com.termux/files/usr/bin
# Çalıştırılacak komut adı
BIN_NAME = kdk

# Renkler
CYAN = \033[0;36m
GREEN = \033[0;32m
RESET = \033[0m

.PHONY: install uninstall

install:
	@echo "$(CYAN)📦 Kurulum Başlıyor$(RESET)"
	@# 1. Bağımlılıkları kontrol et
	@$(PIP) install textual --quiet
	@# 2. Çalıştırılabilir dosyayı oluştur (Shebang + Kod)
	@echo "#!$(BIN_DIR)/python3" > $(BIN_NAME)
	@cat $(APP_NAME) >> $(BIN_NAME)
	@# 3. Yetkileri ayarla ve sisteme taşı
	@chmod +x $(BIN_NAME)
	@mv $(BIN_NAME) $(BIN_DIR)/
	@echo "$(GREEN)✅ Başarıyla kuruldu! Artık her yerden 'kdk' yazabilirsin.$(RESET)"

uninstall:
	@rm -f $(BIN_DIR)/$(BIN_NAME)
	@echo "$(GREEN)🗑️ Sistemden temizlendi.$(RESET)"
