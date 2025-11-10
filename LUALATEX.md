# Миграция с pdfLaTeX на LuaLaTeX

pdfLaTeX – традиционный, но устаревший компилятор LaTeX, плохо поддерживаюющий Unicode и использующий фиксированный шрифты.борка

В оригинальном исходном коде к данному курсу для настройки кодировки и локали обычно используется:

``````latex
\usepackage[utf8]{inputenc}
\usepackage[english,russian]{babel}
% \usepackage[T2A]{fontenc} – встречается часто, но не здесь
``````

LuaLaTeX же не требует использования `inputenc`, заменяет `babel` на `polyglossia` и использует современный `fontspec`:

```latex
\usepackage{fontspec}
\setmainfont{FreeSerif}
\setsansfont{FreeSans}
\setmonofont{FreeMono}

\usepackage{polyglossia}
\setdefaultlanguage{russian}
\setotherlanguage{english}
```

Также необходимо проинструктировать `beamer`:

```latex
\documentclass[lualatex,aspectratio=169]{beamer}
```

Сборка осуществляется скриптом `./build.py`, который заменит все исходные `.pdf`на новые.

Работоспособность проверялась с использованием `LuaHBTeX, Version 1.22.0 (MiKTeX 25.4)` на Windows, репозиторий будет содержать корректные бинарники для уже модифициорванных `.tex` файлов.