---
title: UARTとコンソールを追う
zephyr_version: v4.4.2
source_tag: v4.4.2
last_verified: 2026-09-27
---

# UARTとコンソールを追う

## 出発点

最小の入口は[Hello Worldサンプル](https://github.com/zephyrproject-rtos/zephyr/tree/v4.4.2/samples/hello_world)です。コンソールへ文字を出す経路は、選択したボード、コンソール設定、UARTデバイスのDevicetree記述に依存します。

## ビルド時の接続

1. ボードのDevicetreeがUARTコントローラと、`chosen`ノードに指定されるコンソールを定義します。
2. Kconfigがコンソールとシリアル関連機能を選択します。
3. Devicetree処理が、選ばれたUARTに対応するデバイス参照を生成します。

## 実行時の接続

1. UARTドライバが初期化レベルでデバイスを登録します。
2. コンソール層が、Devicetreeと設定で選択されたデバイスを出力先に結び付けます。
3. `printk()`や標準出力の経路は、設定に応じてコンソールおよびUARTドライバへ到達します。

> **注意: ボード依存の経路**
>
> UARTコントローラ、ピン多重化、コンソールに使うデバイスはボードごとに異なります。説明や検証では必ず対象ボードと最終`zephyr.dts`を併記します。

## 確認方法

```sh
west build -b <board> samples/hello_world
find build -name zephyr.dts -print
git grep -n 'zephyr,console' -- boards dts
```

## 関連項目

- [Devicetree](../04-ビルドと設定/02-Devicetree.md)
- [初期化](../05-カーネル/01-初期化.md)
- [デバイスモデル](../06-ハードウェア抽象化/01-デバイスモデル.md)

## 参照元

- [Hello World sample](https://github.com/zephyrproject-rtos/zephyr/tree/v4.4.2/samples/hello_world)
- [UART API](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/drivers/uart.h)
