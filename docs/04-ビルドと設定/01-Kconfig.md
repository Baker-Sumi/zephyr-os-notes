---
title: Kconfig
zephyr_version: v4.4.2
source_tag: v4.4.2
last_verified: 2026-09-27
---

# Kconfig

## 全体像

Kconfigは、機能を有効化するだけのフラグではありません。シンボルの型、既定値、依存関係、選択関係を解決し、コンパイル時に参照される設定値を作ります。

## 処理の流れ

1. トップレベルの[`Kconfig`](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/Kconfig)が下位のKconfigツリーを取り込みます。
2. アプリケーションの設定断片とボード・SoC由来の設定が、依存関係と共に解決されます。
3. 結果は`build/zephyr/.config`と`build/zephyr/include/generated/zephyr/autoconf.h`へ出力されます。
4. Cコードは`CONFIG_<SYMBOL>`を通じて、条件コンパイルや構成値として利用します。

## 読むときの観点

各シンボルについて、定義場所、`depends on`、`default`、`select`／`imply`、参照するCコードを確認します。`select`は依存関係を満たすことを保証しないため、選択元と選択先の契約を別々に確認します。

## 確認方法

```sh
git grep -n '^config LOG$'
git grep -n 'CONFIG_LOG' -- subsys include drivers
```

## 関連項目

- [ビルドパイプライン](00-ビルドパイプライン.md)
- [ログ](../07-サブシステム/02-ログ.md)

## 参照元

- [トップレベルKconfig](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/Kconfig)
- [logging/Kconfig](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/subsys/logging/Kconfig)
