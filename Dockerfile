# Використовуємо образ domoticz/domoticz:stable
FROM domoticz/domoticz:stable

# Встановлюємо необхідні пакети
RUN apt-get update && apt-get install -y build-essential libffi-dev python3-dev pkg-config libssl-dev

# Оновлюємо до останньої версії pip
RUN pip install --upgrade pip

# Встановлюємо необхідні пакети
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Встановлюємо Rust Compiler
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup install stable

# Встановлюємо необхідні залежності
RUN pip install cryptography requests charset-normalizer paho-mqtt adafruit-blinka adafruit-circuitpython-dht pyserial RPi.GPIO pycryptodome pyaes tinytuya pymodbus==2.5.3

# Копіюємо файли конфігурації або код у контейнер
#COPY ./config /opt/domoticz/userdata

# Встановлюємо робочу директорію
WORKDIR /opt/domoticz

# Встановлюємо entrypoint
ENTRYPOINT ["/opt/domoticz/domoticz", "-dbase", "/opt/domoticz/userdata/domoticz.db", "-log", "/opt/domoticz/userdata/domoticz.log", "-www", "8080", "-sslwww", "443"]
