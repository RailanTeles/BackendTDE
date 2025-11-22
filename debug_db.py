import sqlite3

DB = './database/data.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

at_id = 13
print('\n== Verificando atendimento id=', at_id)
c.execute("SELECT id, data, tipo, numeroPlano, valorTotal, idPaciente, idUsuario FROM atendimentos WHERE id=?", (at_id,))
att = c.fetchone()
print('Atendimento:', att)

print('\n== Procedimentos vinculados:')
c.execute("SELECT idProcedimento FROM Atendimento_Procedimento WHERE idAtendimento=?", (at_id,))
print(c.fetchall())

print('\n== Detalhes procedimentos:')
c.execute('''
SELECT p.id, p.nome, p.valorPlano, p.valorParticular
FROM Atendimento_Procedimento ap
JOIN Procedimentos p ON ap.idProcedimento = p.id
WHERE ap.idAtendimento=?
''', (at_id,))
rows = c.fetchall()
for r in rows:
    print(r)

print('\n== Soma calculada conforme tipo do atendimento:')
if att:
    tipo = att[2]
    c.execute('''
    SELECT COALESCE(SUM(CASE WHEN ? = 'plano' THEN p.valorPlano ELSE p.valorParticular END),0)
    FROM Atendimento_Procedimento ap
    JOIN Procedimentos p ON ap.idProcedimento = p.id
    WHERE ap.idAtendimento=?
    ''', (tipo, at_id))
    print(c.fetchone()[0])
else:
    print('Atendimento não encontrado')

conn.close()
print('\n== FIM')
