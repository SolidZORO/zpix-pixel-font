# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [3.1.7](https://github.com/SolidZORO/zpix-pixel-font/compare/v3.1.6...v3.1.7) (2021-06-29)


### Refactor

* 天(U+5929), 方(U+65b9) ([7c9a696](https://github.com/SolidZORO/zpix-pixel-font/commit/7c9a696b1a21de1cbb53b663adc485e5cce86b2f)), closes [#41](https://github.com/SolidZORO/zpix-pixel-font/issues/41)

### [3.1.6](https://github.com/SolidZORO/zpix-pixel-font/compare/v3.1.5...v3.1.6) (2021-04-19)


### Bug Fixes

* fixed 径 (U+5F84) ([40cc7d5](https://github.com/SolidZORO/zpix-pixel-font/commit/40cc7d5366d1309a933a0b14b0b82c11146d3c02)), closes [#36](https://github.com/SolidZORO/zpix-pixel-font/issues/36)
* fixed 滩 (U+6EE9) ([191ee17](https://github.com/SolidZORO/zpix-pixel-font/commit/191ee17f30a590da4e374e047a93dbe01272e001)), closes [#35](https://github.com/SolidZORO/zpix-pixel-font/issues/35)

### [3.1.5](https://github.com/SolidZORO/zpix-pixel-font/compare/v3.1.4...v3.1.5) (2021-03-16)


### Bug Fixes

* fixed 襄 (U+8944) ([ef4cd6d](https://github.com/SolidZORO/zpix-pixel-font/commit/ef4cd6d8a10656aea652c4461583a36375c4c94b)), closes [#34](https://github.com/SolidZORO/zpix-pixel-font/issues/34)

### [3.1.4](https://github.com/SolidZORO/zpix-pixel-font/compare/v3.1.3...v3.1.4) (2021-01-22)


### Bug Fixes

* fixed 鬥(U+9B25) and 沒(U+6C92) ([30106e2](https://github.com/SolidZORO/zpix-pixel-font/commit/30106e23fcb30f98086dde38cf320828699ddcde)), closes [#32](https://github.com/SolidZORO/zpix-pixel-font/issues/32)

### [3.1.3](https://github.com/SolidZORO/zpix-pixel-font/compare/v3.1.2...v3.1.3) (2020-11-05)


### Refactor

* adjust chinese punctuation ([9a7e02c](https://github.com/SolidZORO/zpix-pixel-font/commit/9a7e02c5d814e47edf5ba39586556cfaf1fb991b))

### [3.1.2](https://github.com/SolidZORO/zpix-pixel-font/compare/v3.1.1...v3.1.2) (2020-11-05)


### Bug Fixes

* adjust the position ：U+FF1A and ；U+FF1B ([5ee3907](https://github.com/SolidZORO/zpix-pixel-font/commit/5ee39074ac1a6450ab76eef22a5a502fb7f03b72)), closes [#27](https://github.com/SolidZORO/zpix-pixel-font/issues/27)


### Refactor

* remove local [@font-face](https://github.com/font-face), use woff2 from vercel host ([2c0a17a](https://github.com/SolidZORO/zpix-pixel-font/commit/2c0a17a41ec3aa91dd7cb5b0626c3d49916ea27f))
* sample website use vercel.app deploy ([4d370ea](https://github.com/SolidZORO/zpix-pixel-font/commit/4d370ead51220d79b8b04a4a6d50036c1a19a608))

### [3.1.1](https://github.com/SolidZORO/zpix-pixel-font/compare/v3.1.0...v3.1.1) (2020-10-08)


### Features

* bdf2ttf build tools ([ef9f9f5](https://github.com/SolidZORO/zpix-pixel-font/commit/ef9f9f5cdf9536a4e97058a1644cba6d34a06981))
* dist dir use git-lfs ([9742938](https://github.com/SolidZORO/zpix-pixel-font/commit/97429383618cbf2edefdad126ea2deb9c8002063))


### Bug Fixes

* fixed 篷 U+7BF7 error ([bda17b6](https://github.com/SolidZORO/zpix-pixel-font/commit/bda17b6b5f464c9db01d3f12bd90adc27587a386)), closes [#26](https://github.com/SolidZORO/zpix-pixel-font/issues/26)


### Refactor

* add build woff2 ([1447d8d](https://github.com/SolidZORO/zpix-pixel-font/commit/1447d8d0d4a2d6236d0bc892dba4c0b8beed5d6d))
* change Font Weight ([77f57f5](https://github.com/SolidZORO/zpix-pixel-font/commit/77f57f5121fe219f7a067091833bfe112e85b4a0))
* minify ttf size ([58c898b](https://github.com/SolidZORO/zpix-pixel-font/commit/58c898b06cd777866ddeef46e8dc2459b095e1ed))
* src only keep .sfd, .bdf and .ttf move to dist dir ([5cb7ac0](https://github.com/SolidZORO/zpix-pixel-font/commit/5cb7ac000f22c544095c55778775f8190c5ccc90))
* update review ([45bdd54](https://github.com/SolidZORO/zpix-pixel-font/commit/45bdd54ef81b7313ae51cec6aaf448fbbce8da52))

## [3.1.0](https://github.com/SolidZORO/zpix-pixel-font/compare/v3.0.2...v3.1.0) (2020-10-08)


### Features

* add standard-version config ([36d1cc3](https://github.com/SolidZORO/zpix-pixel-font/commit/36d1cc3633bc1b6149ef203672a7c3ea26b3f9ad))


## 2.0.0 (skipped)

### Features

* N/A


## [1.2.1](https://github.com/SolidZORO/zpix-pixel-font/compare/v1.2.1...v1.2.1) (2019-09-27)


### Features

* add outline base on pixel! (can be used in any font size now, but it is best to multiples of 12)
* add some full-width characters

### Bug Fixes

* fix some bug
