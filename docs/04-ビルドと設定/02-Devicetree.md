---
title: Devicetree
zephyr_version: v4.4.2
source_tag: v4.4.2
last_verified: 2026-09-27
---

# Devicetree

## 全体像

Devicetreeはハードウェア構成を表す入力であり、ドライバ実装そのものではありません。バインディングがプロパティ契約を定め、処理後に生成されたCマクロを通してアプリケーションやドライバがノードを参照します。

## ディレクトリとファイル

| パス | 役割 |
| --- | --- |
| `boards/` | ボードの基礎Devicetreeとオーバーレイの配置先 |
| `soc/` | SoCのペリフェラルやメモリマップの記述 |
| `dts/bindings/` | `compatible`ごとのプロパティ契約を表すYAML |
| `dts/` | Devicetree処理の共通入力と補助定義 |

## 処理の流れ

1. ボード・SoC・アプリケーションのオーバーレイを合成します。
2. ノードの`compatible`からバインディングを選び、プロパティを検証します。
3. 最終的なツリーとCマクロを生成します。
4. `DT_NODELABEL()`、`DT_ALIAS()`、`DEVICE_DT_GET()`などのマクロが、生成された名前を使ってノード・デバイスへ接続します。

## 確認方法

```sh
west build -b <board> <application>
find build -name zephyr.dts -o -name devicetree_generated.h
```

## 関連項目

- [ビルドパイプライン](00-ビルドパイプライン.md)
- [デバイスモデル](../06-ハードウェア抽象化/01-デバイスモデル.md)
- [GPIO呼び出しを追う](../08-追跡演習/03-GPIO呼び出しを追う.md)

## 参照元

- [dts ディレクトリ](https://github.com/zephyrproject-rtos/zephyr/tree/v4.4.2/dts)
- [Devicetree APIヘッダ](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/devicetree.h)
