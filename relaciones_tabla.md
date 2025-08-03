# 📊 Estructura de Base de Datos - API G Books

## Diagrama de Relaciones

```
    USERS                    BOOK_OWNERS                    BOOKS
┌─────────────┐         ┌─────────────────┐         ┌─────────────┐
│ id (PK)     │◄────────┤ owner_id (FK)   │         │ id (PK)     │
│ username    │         │ book_id (FK)    ├────────►│ title       │
│ email       │         │ date_added      │         │ author      │
│ first_name  │         └─────────────────┘         │ isbn        │
│ last_name   │                                     │ pages       │
│ password    │                                     │ cover       │
│ is_active   │                                     │ language    │
│ ...         │                                     │ description │
└─────────────┘                                     │ available   │
       ▲                                            │ date_added  │
       │                                            └─────────────┘
       │                                                   ▲
       │               READED_BOOKS                        │
       │          ┌─────────────────┐                      │
       └──────────┤ user_id (FK)    │                      │
                  │ book_id (FK)    ├──────────────────────┘
                  │ start           │
                  │ end             │
                  └─────────────────┘
```

## 📋 Tablas y sus Relaciones

### 1. **USERS** (Usuarios)
```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- password
- first_name
- last_name
- is_active
- is_superuser
- is_verified
- date_joined
- birth_date
```

### 2. **BOOKS** (Libros)
```sql
- id (Primary Key)
- title
- author
- published_year
- isbn
- pages
- cover
- language
- description
- available
- date_added
```

### 3. **BOOK_OWNERS** (Tabla de Unión - Propiedad de Libros)
```sql
- id (Primary Key)
- book_id (Foreign Key → books.id)
- owner_id (Foreign Key → users.id)
- date_added
```

### 4. **READED_BOOKS** (Historial de Lectura)
```sql
- id (Primary Key)
- book_id (Foreign Key → books.id)
- user_id (Foreign Key → users.id)
- start (Fecha inicio)
- end (Fecha fin)
```

## 🔗 Tipos de Relaciones

### **Users ↔ Books (Muchos a Muchos)**
- **A través de:** `book_owners`
- **Descripción:** Un usuario puede poseer múltiples libros, y un libro puede ser poseído por múltiples usuarios
- **Uso:** Sistema de biblioteca compartida

### **Users ↔ Books (Muchos a Muchos - Lectura)**
- **A través de:** `readed_books`
- **Descripción:** Un usuario puede leer múltiples libros, y un libro puede ser leído por múltiples usuarios
- **Uso:** Historial y estadísticas de lectura

## 🎯 Casos de Uso

### **Propiedad de Libros**
```python
# Un usuario puede tener múltiples libros
user.owned_books  # → Lista de BookOwner objects

# Un libro puede tener múltiples propietarios
book.owners  # → Lista de BookOwner objects
```

### **Historial de Lectura**
```python
# Registrar que un usuario leyó un libro
ReadedBook(user_id=1, book_id=5, start="2024-01-01", end="2024-01-15")

# Obtener libros leídos por un usuario
SELECT * FROM readed_books WHERE user_id = 1

# Obtener usuarios que leyeron un libro específico
SELECT * FROM readed_books WHERE book_id = 5
```

## 📊 Consultas Comunes

### **Libros de un Usuario**
```sql
SELECT b.* FROM books b
JOIN book_owners bo ON b.id = bo.book_id
WHERE bo.owner_id = ?
```

### **Usuarios que poseen un Libro**
```sql
SELECT u.* FROM users u
JOIN book_owners bo ON u.id = bo.owner_id
WHERE bo.book_id = ?
```

### **Historial de Lectura de un Usuario**
```sql
SELECT b.*, rb.start, rb.end FROM books b
JOIN readed_books rb ON b.id = rb.book_id
WHERE rb.user_id = ?
```

## 🚀 Características del Diseño

- **Escalabilidad:** Soporta múltiples propietarios por libro
- **Flexibilidad:** Separa propiedad de historial de lectura
- **Trazabilidad:** Fechas de adquisición y lectura
- **Integridad:** Foreign Keys mantienen consistencia de datos

## 🔧 Modelos SQLAlchemy

Las relaciones están implementadas usando:
- `relationship()` para navegación entre objetos
- `ForeignKey()` para integridad referencial
- `back_populates` para relaciones bidireccionales

```python
# Ejemplo de relación
class User(Base):
    owned_books = relationship("BookOwner", back_populates="user")

class BookOwner(Base):
    user = relationship("User", back_populates="owned_books")
    book = relationship("Book", back_populates="owners")
```