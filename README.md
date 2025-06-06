# WebServer minimale in Python

**Semplice server HTTP locale** capace di servire un sito statico in **HTML e CSS** a tema _Clash of Clans_, realizzato per il corso universitario di **Programmazione di Reti**.

## 📁 Struttura progetto

- **`server.py`**: server HTTP minimale in Python  
- **`www/`**: directory con i file HTML/CSS/immagini del sito

## ⚙️ Funzionalità

- Gestione richieste **GET**
- Risposta **200 OK** con contenuto del file
- Risposta **404 Not Found** per file mancanti
- Supporto **MIME types** (`.html`, `.css`, `.png`, …)
- **Logging** su console delle richieste

## 🚀 Utilizzo

1. Avvia il server con:  
   ```bash
   python3 server.py
 2.	Apri il browser su: http://localhost:8080 o su http://127.0.0.1:8080
