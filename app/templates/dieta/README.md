# NutriPlan - Planificador de Dietas

NutriPlan es una aplicación web para crear y gestionar planes de dieta semanales. Permite establecer metas, controlar calorías y organizar comidas por día de la semana.

## Características

- Creación y gestión de múltiples dietas
- Seguimiento de calorías y metas
- Organización de comidas por día de la semana
- Interfaz responsiva y minimalista
- Almacenamiento local de datos
- Sin necesidad de servidor o base de datos

## Tecnologías Utilizadas

- HTML5
- CSS3 (con variables CSS y Flexbox/Grid)
- JavaScript (ES6+)
- LocalStorage para persistencia de datos
- Módulos JavaScript
- Diseño Responsivo

## Cómo Usar

1. Abre el archivo `index.html` en tu navegador
2. Haz clic en "Nueva Dieta" para crear un plan
3. Completa los datos de tu dieta:
   - Nombre de la dieta
   - Objetivo de calorías
   - Meta a lograr
   - Comidas por día de la semana
4. Visualiza, edita o elimina tus dietas
5. Consulta el resumen en el panel superior

## Estructura del Proyecto

```
nutriplan/
│
├── index.html          # Página principal
├── app/                # Directorio de la aplicación
│   ├── css/            # Estilos
│   │   └── styles.css  # Hoja de estilos principal
│   ├── js/             # Scripts
│   │   ├── app.js      # Inicialización de la aplicación
│   │   ├── ui.js       # Manejo de la interfaz de usuario
│   │   └── dieta-service.js  # Servicio para operaciones CRUD
│   └── components/     # Componentes reutilizables (si se necesitan)
└── README.md           # Documentación
```

## Funcionalidades CRUD

- **C (Create)**: Crear nuevas dietas con comidas semanales
- **R (Read)**: Ver listado de dietas y detalles de cada una
- **U (Update)**: Modificar dietas existentes y sus comidas
- **D (Delete)**: Eliminar dietas completas

## Instalación

No se requiere instalación. Simplemente descarga los archivos y abre `index.html` en tu navegador.

## Compatibilidad

- Chrome (últimas 2 versiones)
- Firefox (últimas 2 versiones)
- Edge (últimas 2 versiones)
- Safari (últimas 2 versiones)

## Limitaciones

- Los datos se almacenan localmente en el navegador (localStorage)
- No hay sincronización entre dispositivos
- Capacidad de almacenamiento limitada por las restricciones del localStorage

## Licencia

Libre uso y distribución. 