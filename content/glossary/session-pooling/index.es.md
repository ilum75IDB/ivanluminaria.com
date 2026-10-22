---
title: "Session pooling"
description: "Modo de pooling en el que una conexión backend permanece asignada al cliente durante toda la sesión: más compatible pero menos eficiente que el transaction pooling."
translationKey: "glossary_session_pooling"
aka: "Session-level pooling"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

En el session pooling, una conexión backend se reserva para un cliente desde el momento en que se conecta hasta que se desconecta. Es el modo más cercano al comportamiento de una conexión directa y ofrece la mayor compatibilidad con funcionalidades que dependen del estado de sesión: variables `SET`, cursores, tablas temporales y prepared statements con nombre.

## Cómo funciona

El gestor del pool (por ejemplo PgBouncer) asigna una conexión backend al cliente en el momento del login y la mantiene reservada exclusivamente durante toda la sesión. Ningún otro cliente puede utilizarla mientras tanto, aunque el cliente esté idle.

Configuración en PgBouncer:

```ini
[pgbouncer]
pool_mode = session
```

El número máximo de conexiones simultáneas a la base de datos es igual al número de clientes activos, lo que limita la ganancia de eficiencia respecto a las conexiones directas.

## Cuándo utilizarlo

El session pooling es la opción adecuada cuando la aplicación usa funcionalidades que requieren estado de sesión persistente: ORMs que emiten `SET search_path`, drivers que usan prepared statements con nombre, o código legacy que espera que las variables de sesión sobrevivan entre consultas.

Es menos eficiente que el transaction pooling porque el backend permanece ocupado incluso durante los periodos de inactividad del cliente. En escenarios de alta concurrencia, la ventaja principal frente a las conexiones directas es la reducción del overhead de autenticación y del número de procesos backend, no una verdadera multiplexación de conexiones.
