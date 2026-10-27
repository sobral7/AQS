import pytest
from src.desconto import (
    DescontoNormal,
    DescontoPremium,
    DescontoVIP,
    Pedido,
    aplicar_desconto,
)


# Teste Simples com Assert
def test_desconto_normal():
    desconto = DescontoNormal()
    assert desconto.calcular(100.0) == 10.0


# Teste Parametrizado (várias entradas para DescontoPremium)
@pytest.mark.parametrize(
    "valor, esperado",
    [
        (100.0, 30.0),
        (200.0, 60.0),
        (0.0, 0.0),
    ],
)
def test_desconto_premium(valor, esperado):
    desconto = DescontoPremium()
    assert desconto.calcular(valor) == esperado


# Fixture para reutilização do objeto DescontoVIP
@pytest.fixture
def desconto_vip():
    return DescontoVIP()


def test_desconto_vip_calcular(desconto_vip):
    assert desconto_vip.calcular(100.0) == 20.0


def test_desconto_vip_interfaces_especificas(desconto_vip):
    assert desconto_vip.aplicar_cupom("DESCONTO10") is True
    assert desconto_vip.aplicar_cupom("INVALIDO") is False
    assert desconto_vip.validar_usuario_vip("vip") is True


# Teste da classe Pedido (Injeção de Dependência)
def test_pedido_total():
    pedido = Pedido(DescontoNormal())
    assert pedido.total(100.0) == 90.0


# Teste do Princípio de Substituição de Liskov (LSP)
def test_aplicar_desconto_lsp():
    resultado = aplicar_desconto(DescontoVIP(), 100.0)
    assert resultado == 20.0
    