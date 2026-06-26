#!/bin/zsh
# ===================================================================
# bonjour-lan/announce.sh — annuncia uno o più hostname <nome>.local via mDNS
# ===================================================================
# COPIA DI RIFERIMENTO versionata nel repo. La copia ATTIVA vive fuori dal
# repo in ~/Library/Application Support/bonjour-lan/announce.sh ed è condivisa
# da TUTTI i progetti di Ivan (un solo script, N LaunchAgent — uno per progetto).
#
# Uso:   announce.sh <porta> <nome1> [nome2 ...]
# Es.:   announce.sh 1313 ivanluminaria ilum
#
# Effetto: per OGNI <nomeN> pubblica via mDNS un record A "<nomeN>.local" -> IP
# LAN corrente del Mac + un servizio _http._tcp sulla <porta>. Più nomi = alias
# intercambiabili dello stesso servizio. Da un altro device sulla stessa rete:
# http://<nomeN>.local:<porta>
#
# Robustezza: gira in loop; se l'IP LAN cambia (DHCP) ri-annuncia tutti i nomi.
# Pensato per essere lanciato da un LaunchAgent con KeepAlive=true.
# ===================================================================

PORT="$1"
shift
typeset -a NAMES
NAMES=("$@")

if [[ -z "$PORT" || ${#NAMES} -eq 0 ]]; then
    echo "uso: $0 <porta> <nome1> [nome2 ...]" >&2
    exit 64
fi

# Ricava l'IP IPv4 della prima interfaccia LAN attiva (Wi-Fi/Ethernet)
current_ip() {
    local iface ip
    for iface in en0 en1 en2 en3 en4 en5; do
        ip=$(ipconfig getifaddr "$iface" 2>/dev/null)
        if [[ -n "$ip" ]]; then
            print -r -- "$ip"
            return 0
        fi
    done
    return 1
}

typeset -a PIDS
LAST_IP=""

cleanup() {
    local p
    for p in $PIDS; do kill "$p" 2>/dev/null; done
    exit 0
}
trap cleanup TERM INT

echo "[$(date '+%Y-%m-%d %H:%M:%S')] avvio annuncio mDNS porta $PORT, nomi: ${NAMES[*]}"

while true; do
    IP=$(current_ip)
    if [[ -n "$IP" && "$IP" != "$LAST_IP" ]]; then
        # IP nuovo o cambiato: ri-annuncia tutti i nomi
        local p n
        for p in $PIDS; do kill "$p" 2>/dev/null; done
        PIDS=()
        for n in $NAMES; do
            dns-sd -P "$n" _http._tcp local "$PORT" "$n.local" "$IP" &
            PIDS+=($!)
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] annuncio '$n.local' -> $IP:$PORT (dns-sd pid $!)"
        done
        LAST_IP="$IP"
    elif [[ -z "$IP" ]]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] nessuna interfaccia LAN attiva, attendo..."
    fi
    sleep 30
done
