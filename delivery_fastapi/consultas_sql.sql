-- Consultas sql - delivery fastapi

-- Usuários
SELECT * FROM usuarios;

-- Pedidos  
SELECT * FROM pedidos;

-- Itens Pedido
SELECT * FROM itens_pedido;

-- Limpeza (CUIDADO!)
-- DELETE FROM usuarios WHERE id in (1, 2);

-- Estrutura
.schema usuarios
.schema pedidos
.schema itens_pedido

-- Estatísticas
SELECT count(*) as total_usuarios FROM usuarios;
SELECT count(*) as total_pedidos FROM pedidos;
SELECT count(*) as total_itens_pedido FROM itens_pedido;

-- Relacionamentos
SELECT p.*, u.nome, u.email 
FROM pedidos p
JOIN usuarios u ON p.usuario = u.id;

SELECT i.*, p.status, u.nome
FROM itens_pedido i
JOIN pedidos p ON i.pedido = p.id  
JOIN usuarios u ON p.usuario = u.id;

-- extensão vscode -> alexcvzz.vscode-sqlite
-- excuta (CTRL + SHIFT + Q)