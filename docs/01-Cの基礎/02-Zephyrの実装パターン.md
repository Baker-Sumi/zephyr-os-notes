---
title: 組込みCとZephyrの実装パターン
zephyr_version: v4.4.2
source_tag: v4.4.2
last_verified: 2026-09-29
---

# 組込みCとZephyrの実装パターン

## 対象範囲

Zephyrのソースを追うために必要なC、プリプロセッサ、compiler attribute、linker section、実行コンテキストを扱います。C言語そのものの入門、各CPUのABI、特定compilerの最適化指針は扱いません。

## 前提知識

関数、構造体、ポインタ、ビット演算、翻訳単位、静的ライブラリを使ったC開発を前提にします。設定と生成物は[ビルドパイプライン](../04-ビルドと設定/00-ビルドパイプライン.md)を先に確認してください。

## 全体像

Zephyrでは、Cの関数・構造体だけでなく、プリプロセッサとlinkerが静的な登録表を組み立てます。そのため、ソースを読むときは「macroが何へ展開されるか」「どのsectionへ置くか」「誰がそのsectionを走査するか」を分けます。

```mermaid
flowchart LR
    C[C source] --> CPP[preprocessor]
    CPP --> OBJ[object + sections]
    OBJ --> LD[linker]
    LD --> ELF[ELF registration tables]
    ELF --> RT[runtime init / API dispatch]
```

## ディレクトリとファイル

| パス | 重要な記法 | 役割 |
| --- | --- | --- |
| `include/zephyr/sys/util.h` | `CONTAINER_OF`、`IS_ENABLED`など | 広く使うC macroの公開入口 |
| `include/zephyr/toolchain/common.h` | `__syscall`、`BUILD_ASSERT`、`Z_DECL_ALIGN` | toolchain差を吸収し、生成・linker連携用の目印を提供 |
| `include/zephyr/syscall.h` | syscall inline・検証規約 | user modeからkernel実装へ移る呼出の境界 |
| `include/zephyr/init.h` | `SYS_INIT` | 初期化entryを専用sectionへ登録 |
| `include/zephyr/device.h` | `DEVICE_DT_DEFINE` | Devicetree由来のdeviceを定義・初期化登録 |
| `include/zephyr/linker/sections.h` | section名 | C、assembly、linker scriptのsection名を共有 |

## 処理の流れ

1. `CONFIG_*`と`DT_*`は、通常の変数ではなくconfigure時に生成されたC macroです。値の根拠はそれぞれKconfigとDevicetreeに戻って確認します。
2. `IS_ENABLED(CONFIG_FOO)`のようなmacroは、Cの実行時`if`ではなく、macro展開によって設定値を扱います。引数に副作用を入れず、展開後の型・構文を意識します。
3. `CONTAINER_OF(member_ptr, type, member)`は、構造体memberへのポインタから親構造体へのポインタを復元します。memberが本当にその`type`に属するか、寿命が有効かを呼出側で保証します。
4. `BUILD_ASSERT`はcompile時に条件を検査します。ハードウェア状態や初期化成否のような実行時条件には使いません。
5. `SYS_INIT`は`struct init_entry`をlevel・priorityを含むsectionへ置きます。linkerで集められたentryを`kernel/init.c`が実行します。詳細は[初期化](../05-カーネル/01-初期化.md)です。
6. `DEVICE_DT_DEFINE`はdevice object、configuration、API、初期化entryをDevicetree nodeに対応付けます。実行時に`DEVICE_DT_GET`で得るのは、このlink済みobjectです。詳細は[デバイスモデル](../06-ハードウェア抽象化/01-デバイスモデル.md)です。
7. `__syscall`はheaderを解析するbuild scriptの目印にもなります。`CONFIG_USERSPACE`と呼出コンテキストに応じ、direct callまたはkernelへのtrapと検証を使い分けます。

## 設定との対応

| パターン | 依存する条件 | 確認する場所 |
| --- | --- | --- |
| `IS_ENABLED(CONFIG_...)` | Kconfigでsymbolが有効 | `build/zephyr/.config`、`autoconf.h` |
| `DT_*`、`DEVICE_DT_*` | nodeのstatus、binding、driverの有効化 | `zephyr.dts`、generated DT header、driver Kconfig |
| `__syscall` | `CONFIG_USERSPACE`とuser/supervisor context | `include/zephyr/syscall.h`、生成syscall header |
| `SYS_INIT` | init level、priority、linker script | `init.h`、`kernel/init.c`、map file |
| `volatile`、atomic | ISR・thread・hardware registerとの共有規約 | API documentationと呼出コンテキスト |

> **注意: `volatile`は排他制御ではない**
>
> `volatile`はcompilerに対する読み書きの最適化抑制であり、複数threadやISRとの原子性・順序・排他を保証しません。共有データはそのAPIが要求するatomic、spinlock、mutex、semaphore等を選び、ISRから利用可能かを確認します。

## 確認方法

```sh
cd <workspace>/zephyr
git grep -n '#define __syscall' -- include/zephyr
git grep -n '#define BUILD_ASSERT' -- include/zephyr
git grep -n '#define SYS_INIT' -- include/zephyr/init.h
git grep -n '#define DEVICE_DT_DEFINE' -- include/zephyr/device.h
git grep -n 'Z_INIT_ENTRY_SECTION' -- include/zephyr/init.h
```

## 関連項目

- [Kconfig](../04-ビルドと設定/01-Kconfig.md)
- [Devicetree](../04-ビルドと設定/02-Devicetree.md)
- [初期化](../05-カーネル/01-初期化.md)
- [デバイスモデル](../06-ハードウェア抽象化/01-デバイスモデル.md)

## 参照元

- [`sys/util.h` v4.4.2](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/sys/util.h)
- [`toolchain/common.h` v4.4.2](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/toolchain/common.h)
- [`syscall.h` v4.4.2](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/syscall.h)
- [`init.h` v4.4.2](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/init.h)
- [`device.h` v4.4.2](https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/device.h)
