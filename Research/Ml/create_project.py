#!/usr/bin/env python3
import os
import sys
import json
import shutil
from pathlib import Path

# Шаблоны лицензий
LICENSES = {
    "MIT": """MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""",

    "GPL-3.0": """GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2024 Free Software Foundation, Inc.
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.""",

    "GPL-2.0": """GNU GENERAL PUBLIC LICENSE
Version 2, June 1991

Copyright (C) 1989, 1991 Free Software Foundation, Inc.
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.""",

    "LGPL-3.0": """GNU LESSER GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.""",

    "Apache-2.0": """Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.""",

    "BSD-3": """BSD 3-Clause License

Copyright (c) 2024, All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.""",

    "BSD-2": """BSD 2-Clause License

Copyright (c) 2024, All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.""",

    "ISC": """ISC License

Copyright (c) 2024, [fullname]

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.""",

    "Mozilla-2.0": """Mozilla Public License Version 2.0
==================================

1. Definitions
--------------

1.1. "Contributor"
    means each individual or legal entity that creates, contributes to
    the creation of, or owns Covered Software.

1.2. "Contributor Version"
    means the combination of the Contributions of others (if any) used
    by a Contributor and that particular Contributor's Contribution.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.""",

    "AGPL-3.0": """GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.""",

    "CC0-1.0": """Creative Commons Legal Code

CC0 1.0 Universal

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
    PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
    THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
    HEREUNDER.

Statement of Purpose

The laws of most jurisdictions throughout the world automatically confer
exclusive Copyright and Related Rights (defined below) upon the creator
and subsequent owner(s) (each and all, an "owner") of an original work of
authorship and/or a database (each, a "Work").""",

    "CC-BY-4.0": """Creative Commons Attribution 4.0 International Public License

By exercising the Licensed Rights (defined below), You accept and agree
to be bound by the terms and conditions of this Creative Commons
Attribution 4.0 International Public License ("Public License"). To the
extent this Public License may be interpreted as a contract, You are
granted the Licensed Rights in consideration of Your acceptance of
these terms and conditions, and the Licensor grants You such rights in
consideration of benefits the Licensor receives from making the
Licensed Material available under these terms and conditions.""",

    "CC-BY-SA-4.0": """Creative Commons Attribution-ShareAlike 4.0 International Public License

By exercising the Licensed Rights (defined below), You accept and agree
to be bound by the terms and conditions of this Creative Commons
Attribution-ShareAlike 4.0 International Public License ("Public License").
To the extent this Public License may be interpreted as a contract, You are
granted the Licensed Rights in consideration of Your acceptance of
these terms and conditions, and the Licensor grants You such rights in
consideration of benefits the Licensor receives from making the
Licensed Material available under these terms and conditions.""",

    "Unlicense": """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>""",

    "WTFPL": """        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO.""",

    "Zlib": """zlib License

Copyright (c) 2024 <copyright holders>

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.""",

    "Boost": """Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT."""
}


def create_notebook_template(filename):
    """Создает расширенный шаблон Jupyter notebook для анализа данных"""

    # Определяем, является ли файл CSV
    is_csv = True
    file_extension = Path(filename).suffix.lower()

    cells = [
        # Заголовок
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# Анализ данных: {filename}\n",
                "\n",
                "Этот notebook содержит полный анализ данных из файла `{filename}`.\n",
                "\n",
                "## Содержание:\n",
                "1. Загрузка и просмотр данных\n",
                "2. Основная статистика\n",
                "3. Информация о данных\n",
                "4. Анализ пропущенных значений\n",
                "5. Анализ категориальных переменных\n",
                "6. Визуализация данных\n",
                "7. Корреляционный анализ\n"
            ]
        },

        # Импорт библиотек
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Импорт необходимых библиотек\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from scipy import stats\n",
                "import warnings\n",
                "\n",
                "# Настройки для отображения\n",
                "plt.style.use('default')\n",
                "sns.set_palette('husl')\n",
                "pd.set_option('display.max_columns', None)\n",
                "pd.set_option('display.max_rows', 100)\n",
                "warnings.filterwarnings('ignore')\n",
                "\n",
                "print('📊 Библиотеки загружены успешно!')"
            ]
        }
    ]

    # Добавляем специфичные для CSV ячейки
    if is_csv:
        cells.extend([
            # Загрузка данных
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 1. Загрузка и первичный просмотр данных\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"# Загрузка данных из CSV файла\n",
                    f"df = pd.read_csv('{filename}')\n",
                    "\n",
                    "print(f'Данные загружены: {len(df)} строк, {len(df.columns)} столбцов')"
                ]
            },

            # Просмотр данных
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Просмотр первых строк данных\n",
                    "print('Первые 5 строк:')\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Показать весь датафрейм (осторожно с большими данными!)\n",
                    "print('Полный датафрейм:')\n",
                    "df"
                ]
            },

            # Основная статистика
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 2. Основная статистика\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Описательная статистика для числовых переменных\n",
                    "print('📈 Описательная статистика:')\n",
                    "df.describe()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Описательная статистика для всех переменных\n",
                    "print('📊 Статистика для всех типов данных:')\n",
                    "df.describe(include='all')"
                ]
            },

            # Информация о данных
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 3. Информация о структуре данных\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Общая информация о датафрейме\n",
                    "print('ℹ️ Информация о данных:')\n",
                    "df.info()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Типы данных в каждом столбце\n",
                    "print('🔢 Типы данных:')\n",
                    "print(df.dtypes)\n",
                    "print('\\n📏 Размер данных:', df.shape)"
                ]
            },

            # Анализ пропущенных значений
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 4. Анализ пропущенных значений\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Количество пропущенных значений в каждой колонке\n",
                    "print('❌ Пропущенные значения:')\n",
                    "missing_data = df.isnull().sum()\n",
                    "missing_percent = 100 * df.isnull().sum() / len(df)\n",
                    "\n",
                    "missing_table = pd.DataFrame({\n",
                    "    'Пропущено': missing_data,\n",
                    "    'Процент': missing_percent\n",
                    "})\n",
                    "missing_table = missing_table[missing_table['Пропущено'] > 0].sort_values('Пропущено', ascending=False)\n",
                    "\n",
                    "if len(missing_table) > 0:\n",
                    "    print(missing_table)\n",
                    "else:\n",
                    "    print('✅ Пропущенных значений не найдено!')"
                ]
            },

            # Анализ категориальных переменных
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 5. Анализ категориальных переменных\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Анализ уникальных значений для каждой колонки\n",
                    "print('🔍 Уникальные значения в каждой колонке:')\n",
                    "for col in df.columns:\n",
                    "    unique_count = df[col].nunique()\n",
                    "    print(f'{col}: {unique_count} уникальных значений')\n",
                    "    \n",
                    "    # Показываем value_counts для категориальных переменных (менее 20 уникальных значений)\n",
                    "    if unique_count < 20 and unique_count > 1:\n",
                    "        print(f'  Распределение значений:')\n",
                    "        print(df[col].value_counts().head(10))\n",
                    "        print()"
                ]
            },

            # Визуализация данных
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 6. Визуализация данных\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Определяем числовые и категориальные колонки\n",
                    "numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()\n",
                    "categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()\n",
                    "\n",
                    "print(f'📊 Числовые колонки ({len(numeric_cols)}): {numeric_cols}')\n",
                    "print(f'📝 Категориальные колонки ({len(categorical_cols)}): {categorical_cols}')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Гистограммы для числовых переменных\n",
                    "if len(numeric_cols) > 0:\n",
                    "    n_cols = min(3, len(numeric_cols))\n",
                    "    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols\n",
                    "    \n",
                    "    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))\n",
                    "    if n_rows == 1:\n",
                    "        axes = axes.reshape(1, -1)\n",
                    "    if n_cols == 1:\n",
                    "        axes = axes.reshape(-1, 1)\n",
                    "    \n",
                    "    for i, col in enumerate(numeric_cols):\n",
                    "        row, col_idx = divmod(i, n_cols)\n",
                    "        axes[row, col_idx].hist(df[col].dropna(), bins=30, alpha=0.7, edgecolor='black')\n",
                    "        axes[row, col_idx].set_title(f'Распределение: {col}')\n",
                    "        axes[row, col_idx].set_xlabel(col)\n",
                    "        axes[row, col_idx].set_ylabel('Частота')\n",
                    "    \n",
                    "    # Скрываем пустые подграфики\n",
                    "    for i in range(len(numeric_cols), n_rows * n_cols):\n",
                    "        row, col_idx = divmod(i, n_cols)\n",
                    "        axes[row, col_idx].set_visible(False)\n",
                    "    \n",
                    "    plt.tight_layout()\n",
                    "    plt.show()\n",
                    "else:\n",
                    "    print('Числовых переменных для построения гистограмм не найдено.')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Boxplot для числовых переменных\n",
                    "if len(numeric_cols) > 0:\n",
                    "    n_cols = min(3, len(numeric_cols))\n",
                    "    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols\n",
                    "    \n",
                    "    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))\n",
                    "    if n_rows == 1:\n",
                    "        axes = axes.reshape(1, -1)\n",
                    "    if n_cols == 1:\n",
                    "        axes = axes.reshape(-1, 1)\n",
                    "    \n",
                    "    for i, col in enumerate(numeric_cols):\n",
                    "        row, col_idx = divmod(i, n_cols)\n",
                    "        axes[row, col_idx].boxplot(df[col].dropna())\n",
                    "        axes[row, col_idx].set_title(f'Boxplot: {col}')\n",
                    "        axes[row, col_idx].set_ylabel(col)\n",
                    "    \n",
                    "    # Скрываем пустые подграфики\n",
                    "    for i in range(len(numeric_cols), n_rows * n_cols):\n",
                    "        row, col_idx = divmod(i, n_cols)\n",
                    "        axes[row, col_idx].set_visible(False)\n",
                    "    \n",
                    "    plt.tight_layout()\n",
                    "    plt.show()\n",
                    "else:\n",
                    "    print('Числовых переменных для построения boxplot не найдено.')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Столбчатые диаграммы для категориальных переменных\n",
                    "if len(categorical_cols) > 0:\n",
                    "    for col in categorical_cols[:5]:  # Ограничиваем первыми 5 категориальными переменными\n",
                    "        plt.figure(figsize=(12, 6))\n",
                    "        \n",
                    "        # Берем топ-10 значений для отображения\n",
                    "        top_values = df[col].value_counts().head(10)\n",
                    "        \n",
                    "        plt.subplot(1, 2, 1)\n",
                    "        top_values.plot(kind='bar')\n",
                    "        plt.title(f'Топ-10 значений: {col}')\n",
                    "        plt.xticks(rotation=45)\n",
                    "        plt.ylabel('Количество')\n",
                    "        \n",
                    "        plt.subplot(1, 2, 2)\n",
                    "        top_values.plot(kind='pie', autopct='%1.1f%%')\n",
                    "        plt.title(f'Распределение: {col}')\n",
                    "        plt.ylabel('')\n",
                    "        \n",
                    "        plt.tight_layout()\n",
                    "        plt.show()\n",
                    "else:\n",
                    "    print('Категориальных переменных не найдено.')"
                ]
            },

            # Корреляционный анализ
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 7. Корреляционный анализ\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Матрица корреляций для числовых переменных\n",
                    "if len(numeric_cols) > 1:\n",
                    "    correlation_matrix = df[numeric_cols].corr()\n",
                    "    \n",
                    "    plt.figure(figsize=(12, 10))\n",
                    "    sns.heatmap(correlation_matrix, \n",
                    "                annot=True, \n",
                    "                cmap='coolwarm', \n",
                    "                center=0,\n",
                    "                square=True,\n",
                    "                fmt='.2f')\n",
                    "    plt.title('Матрица корреляций', fontsize=16)\n",
                    "    plt.tight_layout()\n",
                    "    plt.show()\n",
                    "    \n",
                    "    # Показываем сильные корреляции\n",
                    "    print('🔗 Сильные корреляции (|r| > 0.7):')\n",
                    "    strong_corr = []\n",
                    "    for i in range(len(correlation_matrix.columns)):\n",
                    "        for j in range(i+1, len(correlation_matrix.columns)):\n",
                    "            corr_val = correlation_matrix.iloc[i, j]\n",
                    "            if abs(corr_val) > 0.7:\n",
                    "                strong_corr.append({\n",
                    "                    'Переменная 1': correlation_matrix.columns[i],\n",
                    "                    'Переменная 2': correlation_matrix.columns[j],\n",
                    "                    'Корреляция': round(corr_val, 3)\n",
                    "                })\n",
                    "    \n",
                    "    if strong_corr:\n",
                    "        strong_corr_df = pd.DataFrame(strong_corr)\n",
                    "        print(strong_corr_df.to_string(index=False))\n",
                    "    else:\n",
                    "        print('Сильных корреляций не найдено.')\n",
                    "        \n",
                    "elif len(numeric_cols) == 1:\n",
                    "    print(f'Найдена только одна числовая переменная: {numeric_cols[0]}')\n",
                    "else:\n",
                    "    print('Числовых переменных для корреляционного анализа не найдено.')"
                ]
            },

            # Заключение
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 8. Заключение\n",
                    "\n",
                    "### Основные выводы:\n",
                    "- Размер данных: укажите количество строк и столбцов\n",
                    "- Качество данных: опишите наличие пропущенных значений\n",
                    "- Ключевые паттерны: опишите найденные закономерности\n",
                    "- Рекомендации: предложите дальнейшие шаги анализа\n",
                    "\n",
                    "### Дальнейшие шаги:\n",
                    "1. Очистка данных (если необходимо)\n",
                    "2. Feature engineering\n",
                    "3. Машинное обучение (если применимо)\n",
                    "4. Создание дашборда или отчета\n"
                ]
            }
        ])
    else:
        # Для других типов файлов создаем базовый шаблон
        cells.extend([
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"## Анализ файла {filename}\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"# Работа с файлом {filename}\n",
                    f"# Адаптируйте код под ваш тип данных\n",
                    "\n",
                    "print('Готов к анализу файла:', '{filename}')"
                ]
            }
        ])

    notebook_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    return json.dumps(notebook_content, indent=2, ensure_ascii=False)


def create_project_structure(filename, license_type):
    """Основная функция создания структуры проекта"""

    # Проверяем существование исходного файла
    if not os.path.exists(filename):
        print(f"Ошибка: файл '{filename}' не найден!")
        return False

    # Проверяем тип лицензии
    if license_type not in LICENSES:
        print(f"Ошибка: неизвестный тип лицензии '{license_type}'")
        print(f"Доступные лицензии: {', '.join(LICENSES.keys())}")
        return False

    # Получаем имя файла без расширения для названия папки
    base_name = Path(filename).stem
    project_dir = f"{base_name}_project"

    try:
        # Создаем папку проекта
        os.makedirs(project_dir, exist_ok=True)
        print(f"Создана папка: {project_dir}")

        # Копируем исходный файл в папку проекта
        dest_file = os.path.join(project_dir, filename)
        shutil.copy2(filename, dest_file)
        print(f"Скопирован исходный файл: {filename}")

        # Создаем файл LICENSE
        license_path = os.path.join(project_dir, "LICENSE")
        with open(license_path, 'w', encoding='utf-8') as f:
            f.write(LICENSES[license_type])
        print(f"Создан файл LICENSE с лицензией: {license_type}")

        # Создаем файл .ipynb
        notebook_name = f"{base_name}.ipynb"
        notebook_path = os.path.join(project_dir, notebook_name)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            f.write(create_notebook_template(base_name))
        print(f"Создан файл Jupyter notebook: {notebook_name}")

        print(f"\nПроект успешно создан в папке: {project_dir}")
        print("Содержимое папки:")
        for item in os.listdir(project_dir):
            print(f"  - {item}")

        return True

    except Exception as e:
        print(f"Ошибка при создании проекта: {e}")
        return False


def main():
    """Главная функция"""
    if len(sys.argv) != 3:
        print("Использование: python script.py <имя_файла> <тип_лицензии>")
        print("Доступные лицензии:", ", ".join(LICENSES.keys()))
        print("Пример: python script.py data.csv MIT")
        sys.exit(1)

    filename = sys.argv[1]
    license_type = sys.argv[2]

    success = create_project_structure(filename, license_type)

    if success:
        print("\n✅ Проект создан успешно!")
    else:
        print("\n❌ Ошибка при создании проекта!")
        sys.exit(1)


if __name__ == "__main__":
    main()