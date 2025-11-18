# 開發紀錄 Changelog

適用於開發者使用 

此文件記錄本專案所有重要的更新與變更。

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## `0.2.0-dev3` ：2025-11-18
### 重構
- 重新組織專案結構，增強元件層級清晰度

    將 UI 元件分為 Components 和 Views，並優化通用模組命名，以提升專案的可擴展性和可維護性。

    主要變更點:
    - 基礎元件 (Controls) 移動到 components/controls/。
    - 視窗/對話框 (Dialogs) 移動到 views/dialogs/。
    - 通用模組 (Common) 重命名為 theme/，專注於樣式。
    - 刪除舊的 controls/ 和 common/ 目錄。"

## `0.2.0-dev2` ：2025-11-18
### 新增
- 新增一種基礎元件：`list_box`。
- 新增字型類別 `TypographyStyle`、`PyLnuixTypography` 貼近實際文字選擇類別。
### 重構
- 新增 `PyLunixStyleSheet` 內各元素文字基礎設定。刪除各元件使用 `.qss`、`.yaml` 控制字型字體。

## `0.2.0-dev1` ：2025-11-11
### 重構
- 新增自製套件 `pylunix-icon-kit` ( 版本 `v1.0.0` ) 
- 刪除原有圖標檔案，改用 `pylunix-icon-kit` 自動生成圖標相關檔案並引用。

## `0.1.1` ： 2025-11-10
### 修正
- 刪除各元件 `.yaml` 含 `ThemeBrush` 相關預設值。
- 修正各透明類型元件 `.qss` 中 `background-color` 直接定義為 `transparent`

##  `0.1.0`  ： 2025-11-08
### 新增
- 新增七種基礎元件：`button`、`check_box`、`hyperlink_button`、`radio_button`、`repeat_button`、`toggle_button`、`tool_button`。
- 新增 `__init__.py` 對各元件導入用 API，現可直接使用 `from pylunix import *`。

---

##  `0.0.2`  ： 2025-11-07
### 初開發版本
- 更新版本號 `0.0.2`。
- 建立 `common`、`config`、`icon_manager`(*測試用*)、`utils`。
- 建立 `path.py` 控制主路徑。

##  `0.0.1`  ： 2025-11-07
### 初開發版本
- 建立版本號 `0.0.1`。
- 建立環境與相關載入包。
- 新增 `README.md` 紀錄主進度。
- 新增 `CHANGELOG.md` 紀錄各版本更新修正。