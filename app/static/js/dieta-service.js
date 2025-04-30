/**
 * Clase para gestionar las operaciones CRUD de dietas
 */
export class DietaService {
    constructor() {
        this.STORAGE_KEY = 'nutriplan_dietas';
    }

    /**
     * Obtiene todas las dietas almacenadas
     * @returns {Array} - Lista de dietas
     */
    obtenerDietas() {
        const dietas = localStorage.getItem(this.STORAGE_KEY);
        return dietas ? JSON.parse(dietas) : [];
    }

    /**
     * Obtiene una dieta por su ID
     * @param {string} id - ID de la dieta
     * @returns {Object|null} - Dieta encontrada o null
     */
    obtenerDietaPorId(id) {
        const dietas = this.obtenerDietas();
        return dietas.find(dieta => dieta.id === id) || null;
    }

    /**
     * Guarda una nueva dieta
     * @param {Object} dieta - Datos de la dieta a guardar
     * @returns {Object} - Dieta guardada con ID generado
     */
    guardarDieta(dieta) {
        const dietas = this.obtenerDietas();
        
        // Generar ID único si es una nueva dieta
        if (!dieta.id) {
            dieta.id = this._generarId();
            dieta.fechaCreacion = new Date().toISOString();
        } else {
            // Si es una actualización, mantener la fecha de creación original
            const dietaOriginal = dietas.find(d => d.id === dieta.id);
            if (dietaOriginal) {
                dieta.fechaCreacion = dietaOriginal.fechaCreacion;
            } else {
                dieta.fechaCreacion = new Date().toISOString();
            }
        }
        
        // Actualizar fecha de modificación
        dieta.fechaModificacion = new Date().toISOString();
        
        // Añadir o actualizar la dieta
        const nuevasDietas = dietas.filter(d => d.id !== dieta.id);
        nuevasDietas.push(dieta);
        
        // Guardar en localStorage
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(nuevasDietas));
        
        return dieta;
    }

    /**
     * Elimina una dieta por su ID
     * @param {string} id - ID de la dieta a eliminar
     * @returns {boolean} - true si se eliminó correctamente
     */
    eliminarDieta(id) {
        const dietas = this.obtenerDietas();
        const nuevasDietas = dietas.filter(dieta => dieta.id !== id);
        
        // Si el tamaño de los arrays es diferente, se eliminó algo
        if (nuevasDietas.length !== dietas.length) {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(nuevasDietas));
            return true;
        }
        
        return false;
    }

    /**
     * Obtiene estadísticas generales de todas las dietas
     * @returns {Object} - Objeto con estadísticas
     */
    obtenerEstadisticas() {
        const dietas = this.obtenerDietas();
        let totalCalorias = 0;
        let totalComidas = 0;
        
        dietas.forEach(dieta => {
            totalCalorias += parseInt(dieta.objetivoCalorias || 0);
            totalComidas += dieta.comidas?.length || 0;
        });
        
        // Calcular el progreso general (si hay dietas)
        const progresoMeta = dietas.length > 0 
            ? Math.round((totalComidas / (dietas.length * 7)) * 100) // Asumimos 7 comidas por semana ideal
            : 0;
        
        return {
            totalDietas: dietas.length,
            totalCalorias,
            totalComidas,
            progresoMeta
        };
    }

    /**
     * Genera un ID único basado en timestamp y valor aleatorio
     * @returns {string} - ID generado
     * @private
     */
    _generarId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
    }
} 