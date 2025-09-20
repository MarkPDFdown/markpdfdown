# Changelog

## [1.1.2] - 2025-09-20
### :bug: Bug Fixes
- [`c5d1a6a`](https://github.com/MarkPDFdown/markpdfdown/commit/c5d1a6a02c4e89e7b609dd3df275f13659b2d917) - Fix missing RUST compiler issue when building fastuuid in CI environment *(commit by [@jorben](https://github.com/jorben))*

### :wrench: Chores
- [`fbb1a6d`](https://github.com/MarkPDFdown/markpdfdown/commit/fbb1a6d4b8434468c950cac6d3180c80eae7e741) - update version *(commit by [@jorben](https://github.com/jorben))*


## [1.1.1] - 2025-09-20
### :bug: Bug Fixes
- [`7bf7005`](https://github.com/MarkPDFdown/markpdfdown/commit/7bf70053d33999ab56cfca27576bd7f6676c91d5) - update dockerfile, fix uv path issue *(commit by [@jorben](https://github.com/jorben))*

### :wrench: Chores
- [`ff966b4`](https://github.com/MarkPDFdown/markpdfdown/commit/ff966b4ffb4a79316e5b411075d22a4e20211a49) - update version *(commit by [@jorben](https://github.com/jorben))*


## [1.1.0] - 2025-09-20
### :recycle: Refactors
- [`da51adf`](https://github.com/MarkPDFdown/markpdfdown/commit/da51adf932ffaf05e17d7324ccddbdad8f9f8500) - The project was comprehensively refactored, with litellm introduced as the LLM client library, and input/output parameters were optimized. *(commit by [@jorben](https://github.com/jorben))*

## [1.0.11] - 2025-09-02
### :sparkles: New Features
- [`1f6915f`](https://github.com/MarkPDFdown/markpdfdown/commit/1f6915f9006d50d845f1ad806ba1dcb58cd6a695) - Add multilingual README translations *(PR [#22](https://github.com/MarkPDFdown/markpdfdown/pull/22) by [@clearclown](https://github.com/clearclown))*
- [`af25adb`](https://github.com/MarkPDFdown/markpdfdown/commit/af25adbea39dd57f155e7d6feeb9dd18ade68495) - Add reasoning_effort parameter support *(commit by [@jorben](https://github.com/jorben))*

[1.0.11]: https://github.com/MarkPDFdown/markpdfdown/compare/1.0.10...1.0.11
[1.1.0]: https://github.com/MarkPDFdown/markpdfdown/compare/1.0.11...1.1.0
[1.1.1]: https://github.com/MarkPDFdown/markpdfdown/compare/1.1.0...1.1.1

## Version: 1.0.8

* [#15](https://github.com/MarkPDFdown/markpdfdown/pull/15): fix: Fixed the issue where hunyuan does not support empty system_prompt

## Version: 1.0.7

* [#8](https://github.com/MarkPDFdown/markpdfdown/pull/8): fix: Fix the path spelling error in the Readme
* [#11](https://github.com/MarkPDFdown/markpdfdown/pull/11): fix: Fix the OpenAI API 400 Bad Request issue #10

## [1.0.6](https://github.com/jorben/markpdfdown/compare/1.0.5...1.0.6)

> 24 March 2025

- chore: Compress demo images [`9062d01`](https://github.com/jorben/markpdfdown/commit/9062d01644ac098da41c9f4450b1217d9728e2b3)
- chore: Emphasize the use of LaTeX syntax for mathematical formulas [`2aef544`](https://github.com/jorben/markpdfdown/commit/2aef5448cece60efbc03d40ad5d05b7d5e9877d1)
- chore: Add ChangeLog action [`3587a00`](https://github.com/jorben/markpdfdown/commit/3587a007c242b857586b2beb8a1e105743713a45)

## [1.0.5](https://github.com/jorben/markpdfdown/compare/1.0.4...1.0.5)

> 22 March 2025

- refactor: Refactor PDFWorker, build a FileWorker base class to facilitate future extension for supporting more file types [`d4e6398`](https://github.com/jorben/markpdfdown/commit/d4e6398e9ea0f59d1c512b9e35ef5efc2fd117cd)
- feat: Added support for converting images (JPG/PNG/BMP) to Markdown #6 [`1eab0db`](https://github.com/jorben/markpdfdown/commit/1eab0db854ba8669d8107edf74aac645430f71d0)

## [1.0.4](https://github.com/jorben/markpdfdown/compare/1.0.3...1.0.4)

> 20 March 2025

- chore: Add Chinese introduction [`d1a9a69`](https://github.com/jorben/markpdfdown/commit/d1a9a69f60b378e1f899fcc7c874ab1ae185edf5)
- feat: Add and remove markdown wrapping and corresponding unit test cases [`c75fb71`](https://github.com/jorben/markpdfdown/commit/c75fb71f9e8ed0db781fbba93ce27050ef3c097d)
- chore: Modify Readme [`b6c0208`](https://github.com/jorben/markpdfdown/commit/b6c020859a570731e9a31ddf8e1de618eeeba2b2)

## [1.0.3](https://github.com/jorben/markpdfdown/compare/1.0.2...1.0.3)

> 15 March 2025

- chore: The default settings are for the OpenAI API and the GPT-4 model. [`5f0bef0`](https://github.com/jorben/markpdfdown/commit/5f0bef0d04fe83b79a188385613d84b2d6bf1c5f)
- chore: Add effect demonstration images to the Readme [`cb6e317`](https://github.com/jorben/markpdfdown/commit/cb6e317c2247f8df9572f26dc758f8faa7e5280f)
- fix: Fix the "the input device is not a TTY" error in docker run [`4359f4b`](https://github.com/jorben/markpdfdown/commit/4359f4b21ee0d5460b110db36809f689d5367264)

## [1.0.2](https://github.com/jorben/markpdfdown/compare/1.0.1...1.0.2)

> 15 March 2025

- fix: Fix the build image pipeline error on the armv7 platform [`afa0f61`](https://github.com/jorben/markpdfdown/commit/afa0f6191413166bc8ed2ad28db2defd40d0d199)

## [1.0.1](https://github.com/jorben/markpdfdown/compare/1.0.0...1.0.1)

> 15 March 2025

- fix: Fix the build image pipeline error on the 386 platform [`7012440`](https://github.com/jorben/markpdfdown/commit/7012440a3a0af55a901ca5bad6495a05a4509456)

## 1.0.0

> 15 March 2025

- Initial commit [`58eac07`](https://github.com/jorben/markpdfdown/commit/58eac0798ec6ea4b521ddc060284489e27a42ca0)
- chore: Updated some content [`8f5c533`](https://github.com/jorben/markpdfdown/commit/8f5c5339a6ca5690266f2a97223c410b4ef6b168)
- chore: Add LLMClient, PDFWork class and implementation [`b040a48`](https://github.com/jorben/markpdfdown/commit/b040a4878957f76baa51db4f958b52b1eeb1bb38)

















[1.1.2]: https://github.com/MarkPDFdown/markpdfdown/compare/1.1.1...1.1.2
