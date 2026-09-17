using System.Text;

/// Historial circular de los últimos golpes, sin asignaciones.
///
/// Se guarda como datos y NO como texto. Formatear una cadena por golpe asignaría memoria en
/// el camino caliente, y en este proyecto eso está prohibido por una razón medida: el
/// recolector de basura produce caídas de frame, y sin la predicción del plano armado el
/// jitter se triplicaba por cuantización de frame. El texto se arma aparte, a ritmo de
/// pantalla, que es mil veces menos frecuente.
public sealed class HitRing
{
    public struct Entrada
    {
        public string Pieza;
        public int Intensidad;
        public float Velocidad;
    }

    readonly Entrada[] buffer;
    int siguiente;
    int cuantos;

    public HitRing(int capacidad)
    {
        buffer = new Entrada[capacidad < 1 ? 1 : capacidad];
    }

    public int Capacidad => buffer.Length;
    public int Cuantos => cuantos;

    /// Sin asignaciones: solo escribe en el arreglo ya reservado.
    public void Agregar(string pieza, int intensidad, float velocidad)
    {
        buffer[siguiente] = new Entrada { Pieza = pieza, Intensidad = intensidad, Velocidad = velocidad };
        siguiente = (siguiente + 1) % buffer.Length;
        if (cuantos < buffer.Length) cuantos++;
    }

    /// 0 es el más reciente.
    public Entrada Reciente(int atras)
    {
        if (atras < 0 || atras >= cuantos) return default;
        int i = siguiente - 1 - atras;
        if (i < 0) i += buffer.Length;
        return buffer[i];
    }

    /// Escribe el historial en el StringBuilder que se le pasa, del más reciente al más viejo.
    /// Recibe el StringBuilder en lugar de devolver una cadena para no asignar en cada refresco.
    public void Describir(StringBuilder sb)
    {
        sb.Clear();
        for (int k = 0; k < cuantos; k++)
        {
            var e = Reciente(k);
            sb.Append(e.Pieza);
            for (int s = e.Pieza != null ? e.Pieza.Length : 0; s < 10; s++) sb.Append(' ');
            for (int p = 1; p <= 3; p++) sb.Append(p <= e.Intensidad ? '●' : '○');
            sb.Append("  ").Append(e.Velocidad.ToString("F1")).Append(" m/s");
            if (k < cuantos - 1) sb.Append('\n');
        }
    }
}
