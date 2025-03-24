// Importar módulos
import { DietaService } from 'static/js/dieta-service.js';
import { UI } from 'static/js/ui.js';

// Inicializar la aplicación cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', () => {
    // Instanciar servicios
    const dietaService = new DietaService();
    const ui = new UI(dietaService);
    
    // Inicializar la interfaz
    ui.init();
    
    // Cargar y mostrar las dietas almacenadas
    ui.cargarDietas();
    
    // Actualizar el resumen
    ui.actualizarResumen();
}); 