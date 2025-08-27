# Paw&Whiskers
Creado por Samuel Deossa y Maria Antonia Muñoz.

# En que consiste nuestro proyecto
Consiste en el desarrollo de una tienda virtual específicamente de productos para perros y gatos.
Esta plataforma permitirá a los usuarios adquirir de manera fácil y rápida una gran variedad de artículos tales como comida, juguetes, accesorios y ropa para sus mascotas.
El objetivo principal es crear una solución eficiente para los dueños de mascotas, conectándolos con productos de calidad, optimizando el proceso de compra y mejorando la experiencia de usuario


# Guía de Estilo y Reglas de Programación - Paw&Whiskers

Este documento define las reglas de estilo y programación que deben seguirse en el proyecto **Paw&Whiskers**.  
Si un compañero envía un push que no cumpla estas reglas, deberá ser remitido nuevamente a esta guía.  

---

## 1. Guía de estilo general

### 1.1 Idioma
- Todo el código debe estar en **español** (variables, funciones, clases, comentarios, templates).  
- Se permite inglés solo para nombres reservados o librerías externas.  

### 1.2 Nombres de variables y funciones
- Usar **snake_case** (`palabras_en_minusculas_con_guion_bajo`).  
- Los nombres deben ser **descriptivos y claros**.  

### 1.3 Nombres de clases y modelos
- Usar **CamelCase** (`PrimeraLetraEnMayúscula`).  
- Los nombres deben representar **entidades del negocio**.  

### 1.4 Comentarios y documentación
- Cada función o clase debe tener un comentario breve en **español** explicando su propósito.  

### 1.5 Organización de archivos
- `models.py` → Definir entidades del negocio.  
- `views.py` → Lógica de interacción usuario ↔ sistema.  
- `urls.py` → Definir rutas y conectarlas con vistas.  
- `templates/` → Archivos HTML extendiendo siempre de `base.html`.  
- `static/` → Archivos estáticos (CSS, imágenes, JS).  

### 1.6 Estilo en HTML/CSS
- Indentación de **4 espacios**.  
- Usar clases **semánticas y consistentes**.  

### 1.7 Buenas prácticas en lógica
- Evitar duplicación de código (**DRY: Don’t Repeat Yourself**).  
- Evitar números mágicos (usar **constantes con nombres claros**).  

---

## 2. Reglas técnicas por capas

### 2.1 Rutas (`urls.py`)
- Toda ruta debe estar asociada a una **View**.  
- Los nombres de las rutas deben ser **descriptivos y en español**.  

### 2.2 Vistas (`views.py`)
- Cada vista debe **extender de `base.html`**.  
- Usar funciones o clases claras, con **nombres descriptivos**.  
- No mezclar lógica de negocio en las vistas (usar **modelos y helpers**).  

### 2.3 Modelos (`models.py`)
- Los modelos deben representar **entidades reales del negocio**.  
- Usar nombres en **singular** (`Producto`, no `Productos`).  
- Cada modelo debe tener su método `__str__` para representar objetos de manera legible.  

### 2.4 Templates (`templates/`)
- Todos los templates deben ser **HTML válidos**.  
- Siempre extender de `base.html` para mantener consistencia.  
- Usar bloques de Django `{% block content %}` para contenido principal.  

### 2.5 Controladores / Lógica
- Toda la lógica debe estar **separada en funciones reutilizables**.  
- Evitar lógica compleja en los templates.  
- Validar datos en las vistas antes de guardar en los modelos.  

---

## 3. Versionamiento y colaboración

- Todo **push al repositorio** debe cumplir estas reglas.  
- Si un compañero sube código que no cumpla con esta guía, debe corregirlo antes de fusionar.  

---

Con estas reglas tendremos un proyecto ordenado, consistente y fácil de mantener.  
