---
title: GPIO呼び出しを追う
zephyr_version: v4.4.2
source_tag: v4.4.2
last_verified: 2026-09-27
---

# GPIO呼び出しを追う

## 出発点

公式の[Blinkyサンプル](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/samples/basic/blinky/src/main.c)は、`led0`エイリアスからLEDのGPIOを取得し、初期化して反転します。

```c
#define LED0_NODE DT_ALIAS(led0)
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);
```

## ビルド時の接続

1. `DT_ALIAS(led0)`は[`include/zephyr/devicetree.h`](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/devicetree.h#L237)で、Devicetreeから生成されたエイリアスマクロを参照します。
2. `GPIO_DT_SPEC_GET()`は、ノードの`gpios`プロパティを`struct gpio_dt_spec`の初期化子へ変換します。定義は[`gpio.h`](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/drivers/gpio.h#L339-L377)です。
3. `gpio_dt_spec`にはGPIOコントローラのデバイス、ピン番号、フラグが含まれます。どのGPIOコントローラになるかは、選んだボードのDevicetreeに依存します。

## 実行時の接続

1. `gpio_is_ready_dt(&led)`で、関連付いたGPIOコントローラが初期化済みか確認します。
2. `gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE)`が、指定ピンを出力として構成します。
3. `gpio_pin_toggle_dt(&led)`が、`led.port`にあるドライバAPIを通じてピン状態を反転します。
4. GPIOコントローラの実装は、対象SoCに対応する`drivers/gpio/`のファイルで`DEVICE_DT_DEFINE()`などにより登録されます。

## 確認方法

```sh
git show v4.4.2:samples/basic/blinky/src/main.c
git grep -n 'gpio_pin_toggle_dt' -- include/zephyr/drivers/gpio.h
git grep -n 'DEVICE_DT_DEFINE' -- drivers/gpio | head
```

## 関連項目

- [Devicetree](../04-ビルドと設定/02-Devicetree.md)
- [デバイスモデル](../06-ハードウェア抽象化/01-デバイスモデル.md)

## 参照元

- [Blinky main.c](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/samples/basic/blinky/src/main.c)
- [GPIO API](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/drivers/gpio.h)
