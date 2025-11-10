# 開發紀錄 Changelog

適用於開發者使用 

此文件記錄本專案所有重要的更新與變更。

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## `0.2.0-dev2` ( 開發預定：2025-11-X )
### 新增
- 新增基礎元件：`list_box`、`buttons`(button_group)、`radio_buttons`...等。

## `0.2.0-dev1` ( 開發預定：2025-11-10 )
### 重構
- 重構 `.yaml` 相關處理，各元件 `.yaml` 新增預設值預防無法正確找到對應色值。

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