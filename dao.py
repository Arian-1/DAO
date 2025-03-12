from abc import ABC, abstractmethod


# Entidad: User
class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.name} | Email: {self.email}"


# Interfaz DAO: Define las operaciones básicas para la entidad User
class UserDAO(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def insert(self, user: User) -> None:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        pass


# Implementación concreta del DAO usando almacenamiento en memoria
class InMemoryUserDAO(UserDAO):
    def __init__(self):
        self.users = {}

    def get_by_id(self, user_id: int) -> User:
        return self.users.get(user_id)

    def get_all(self) -> list:
        return list(self.users.values())

    def insert(self, user: User) -> None:
        if user.id in self.users:
            raise Exception("El usuario con este ID ya existe.")
        self.users[user.id] = user

    def update(self, user: User) -> None:
        if user.id in self.users:
            self.users[user.id] = user
        else:
            raise Exception("Usuario no encontrado para actualizar.")

    def delete(self, user: User) -> None:
        if user.id in self.users:
            del self.users[user.id]
        else:
            raise Exception("Usuario no encontrado para borrar.")


# Función para mostrar el menú interactivo
def mostrar_menu():
    print("\n=== Menú de Gestión de Usuarios ===")
    print("1. Listar usuarios")
    print("2. Crear usuario")
    print("3. Actualizar usuario")
    print("4. Eliminar usuario")
    print("5. Salir")


# Función principal que integra la lógica de negocio con la interfaz de usuario
def main():
    user_dao = InMemoryUserDAO()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            # Listar usuarios
            usuarios = user_dao.get_all()
            if usuarios:
                print("\nLista de usuarios:")
                for usuario in usuarios:
                    print(usuario)
            else:
                print("\nNo hay usuarios registrados.")

        elif opcion == '2':
            # Crear usuario
            try:
                id_input = int(input("Ingrese ID del usuario: "))
                name_input = input("Ingrese el nombre: ")
                email_input = input("Ingrese el email: ")
                nuevo_usuario = User(id_input, name_input, email_input)
                user_dao.insert(nuevo_usuario)
                print("\nUsuario creado exitosamente.")
            except ValueError:
                print("Error: El ID debe ser un número entero.")
            except Exception as e:
                print("Error:", e)

        elif opcion == '3':
            # Actualizar usuario
            try:
                id_input = int(input("Ingrese el ID del usuario a actualizar: "))
                usuario_existente = user_dao.get_by_id(id_input)
                if usuario_existente:
                    print("Datos actuales:", usuario_existente)
                    name_input = input("Ingrese el nuevo nombre (dejar en blanco para no cambiar): ")
                    email_input = input("Ingrese el nuevo email (dejar en blanco para no cambiar): ")
                    if name_input.strip() == "":
                        name_input = usuario_existente.name
                    if email_input.strip() == "":
                        email_input = usuario_existente.email
                    usuario_actualizado = User(id_input, name_input, email_input)
                    user_dao.update(usuario_actualizado)
                    print("\nUsuario actualizado exitosamente.")
                else:
                    print("No se encontró un usuario con ese ID.")
            except ValueError:
                print("Error: El ID debe ser un número entero.")
            except Exception as e:
                print("Error:", e)

        elif opcion == '4':
            # Eliminar usuario
            try:
                id_input = int(input("Ingrese el ID del usuario a eliminar: "))
                usuario_existente = user_dao.get_by_id(id_input)
                if usuario_existente:
                    user_dao.delete(usuario_existente)
                    print("\nUsuario eliminado exitosamente.")
                else:
                    print("No se encontró un usuario con ese ID.")
            except ValueError:
                print("Error: El ID debe ser un número entero.")
            except Exception as e:
                print("Error:", e)

        elif opcion == '5':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
