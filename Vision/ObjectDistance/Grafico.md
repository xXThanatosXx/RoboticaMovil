# Taxonomía del Marco Teórico y Conceptual

```plantuml
@startuml
class Investigacion {
  - Nombre: string
  - Objetivos: list
  - Pregunta: string
}

class Tema {
  - Nombre: string
  - Descripcion: string
}

class Subtema {
  - Nombre: string
  - Descripcion: string
}

Investigacion "1" -- "n" Tema : contiene
Tema "1" -- "n" Subtema : contiene
@enduml
