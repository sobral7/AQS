from abc import ABC, abstractmethod


# ==============================================================================
# 1. INTERFACES ESPECÍFICAS (ISP - Interface Segregation Principle)
# ==============================================================================
class IDesconto(ABC):

  @abstractmethod
  def calcular(self, valor: float) -> float:
    pass


class ICupom(ABC):

  @abstractmethod
  def aplicar_cupom(self, codigo: str) -> bool:
    pass


class IVIP(ABC):

  @abstractmethod
  def validar_usuario_vip(self, usuario: str) -> bool:
    pass


# ==============================================================================
# 2. IMPLEMENTAÇÕES DA INTERFACE
# ==============================================================================
class DescontoNormal(IDesconto):

  def calcular(self, valor: float) -> float:
    return valor * 0.1


class DescontoVIP(IDesconto, ICupom, IVIP):

  def calcular(self, valor: float) -> float:
    return valor * 0.2

  def aplicar_cupom(self, codigo: str) -> bool:
    return codigo == "DESCONTO10"

  def validar_usuario_vip(self, usuario: str) -> bool:
    return usuario == "vip"


class DescontoPremium(IDesconto):

  def calcular(self, valor: float) -> float:
    return valor * 0.3


# ==============================================================================
# 3. FUNÇÃO AUXILIAR (LSP - Liskov Substitution Principle)
# ==============================================================================
def aplicar_desconto(desconto: IDesconto, valor: float) -> float:
  # Aceita qualquer subclasse de IDesconto de forma transparente
  return desconto.calcular(valor)


# ==============================================================================
# 4. CLASSE PEDIDO (DIP - Dependency Inversion Principle)
# ==============================================================================
class Pedido:

  def __init__(self, desconto: IDesconto):
    # Depende da abstração IDesconto e não de uma implementação concreta
    self.desconto = desconto

  def total(self, valor: float) -> float:
    return valor - self.desconto.calcular(valor)


# ==============================================================================
# EXECUÇÃO DA APLICAÇÃO
# ==============================================================================
def main():
  valor = 100.0

  # Testando DIP (Injeção de dependência no Pedido)
  pedido_normal = Pedido(DescontoNormal())
  pedido_vip = Pedido(DescontoVIP())

  print(f"Total Pedido Normal: R$ {pedido_normal.total(valor):.2f}")
  print(f"Total Pedido VIP: R$ {pedido_vip.total(valor):.2f}")

  # Testando LSP (Substituição de Liskov)
  desconto_valor = aplicar_desconto(DescontoPremium(), valor)
  print(f"Valor do Desconto Premium: R$ {desconto_valor:.2f}")

  # Testando ISP (Uso de interfaces específicas do VIP)
  vip = DescontoVIP()
  print(f"Cupom aplicado: {vip.aplicar_cupom('DESCONTO10')}")
  print(f"Status do usuário: {vip.validar_usuario_vip('vip')}")


if __name__ == "__main__":
  main()