from sklearn.experimental import enable_iterative_imputer  
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="Northwind",
    user="postgres",
    password="postgres123",
    host="localhost",
    port="5432"
)

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost/Northwind"

engine = create_engine(DATABASE_URL)


query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public';
"""
df_tables = pd.read_sql(query, conn)
print("Tables in the Database:")
print(df_tables)

## ¿Cuántos empleados tenemos contratados en 'Global Importaciones'?

query1 = """
SELECT e.employee_id, e.first_name, e.last_name, e.city, e.country
FROM employees e
"""

# Read into a DataFrame
df = pd.read_sql(query1, conn)
#print(df.info())
print(df.head())

## ¿Qué productos tenemos?

query2 = """
SELECT p.product_id, p.supplier_id, p.product_name, p.units_in_stock, p.units_on_order, p.discontinued
FROM products p
"""
df_products = pd.read_sql(query2, conn)
print(df_products.head())

##¿Tenemos productos discontinuados?

query3 = """
SELECT product_name, units_in_stock 
FROM products 
WHERE discontinued = 1
ORDER BY units_in_stock ASC;
"""
df_discontinued = pd.read_sql(query3, conn)
print(df_discontinued.head())

##¿Qué proveedores tenemos?

query4 = """
SELECT supplier_id, company_name, city, country
FROM suppliers
"""
df = pd.read_sql(query4, conn)
print(df.head())


## ¿Qué pedidos hemos tenido?

query5 = """
SELECT order_id, customer_id, employee_id, order_date, required_date, shipped_date
FROM orders
"""
df = pd.read_sql(query5, conn)
print(df.head())
#Sé que shipped_date es la fecha en la que se envía, pero no sé como clacular la fecha de entrega


## ¿Cuántos pedidos hemos tenido?

query6 = """
SELECT COUNT(order_id) AS total_pedidos
FROM orders;
"""
df = pd.read_sql(query6, conn)
print(df)

## ¿Cuántos clientes tenemos?

query7 = """
SELECT 
    COUNT(DISTINCT o.customer_id) AS total_clientes, 
    s.company_name,
    s.city,
    s.country
FROM Orders o
JOIN Order_Details od ON o.order_id = od.order_id
JOIN Products p ON od.product_id = p.product_id
JOIN Suppliers s ON p.supplier_id = s.supplier_id
GROUP BY s.company_name, s.city, s.country;
"""
df_customers = pd.read_sql(query7, conn)
print(df_customers)


## ¿Con qué empresas de transporte trabajamos?

query8 = """
SELECT 
    s.company_name,
	o.employee_id
FROM Orders o
JOIN Order_Details od ON o.order_id = od.order_id
JOIN Products p ON od.product_id = p.product_id
JOIN Suppliers s ON p.supplier_id = s.supplier_id
GROUP BY s.company_name, o.employee_id;
"""
df_tpt = pd.read_sql(query8, conn)
print(df_tpt)

## ¿Cómo son las relaciones de reporte de resultados entre los empleados?

query9 = """
SELECT 
    e.employee_id AS empleado,
    e.first_name || ' ' || e.last_name AS nombre_empleado,
    m.employee_id AS id_jefe,
    m.first_name || ' ' || m.last_name AS nombre_jefe
FROM employees e
LEFT JOIN employees m ON e.reports_to = m.employee_id
ORDER BY e.employee_id;
"""
df_employees = pd.read_sql(query9, conn)
print(df_employees)


##### EJERCICIO 3 #####

## Estudio de evolución
query10 = """
SELECT 
    TO_CHAR(order_date, 'MM') AS mes, 
    TO_CHAR(order_date, 'YYYY') AS año, 
    COUNT(*) AS total_pedidos
FROM orders
GROUP BY año, mes
ORDER BY año, mes;
"""
df = pd.read_sql(query10, conn)

print(df.head())  
print(df.columns)

# Crear una columna de fecha con formato 'YYYY-MM'
df['fecha'] = pd.to_datetime(df['año'] + '-' + df['mes'] + '-01')

# Generar gráfico usando MATPLOTLIB
plt.figure(figsize=(12, 6))
plt.plot(df['fecha'], df['total_pedidos'], linestyle='-', color='b', label='Pedidos')

# Personalizar gráfico
plt.xlabel("Fecha (Año-Mes)")
plt.ylabel("Total de Pedidos")
plt.title("Evolución de Pedidos por Mes")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

plt.show()


# Generar gráfico usando PLOTLY
fig = px.line(df, x='fecha', y='total_pedidos', 
              markers=True, #activa los puntos en la línea del gráfico, automáticamente usa círculos en cada punto de la línea.
              title="Evolución de Pedidos por Mes",
              labels={'fecha': 'Fecha (Año-Mes)', 'total_pedidos': 'Total Pedidos'}
              )

fig.show()




## Estudio de países con más ventas

'''
query11 = """
SELECT 
    c.country, 
    COUNT(o.order_id) AS total_pedidos
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.country
ORDER BY total_pedidos DESC;
"""
df = pd.read_sql(query11, conn)

continentes = {'Europe': ['Austria', 'Belgium', 'Denmark', 'Finland', 'France',
'Germany', 'Ireland', 'Italy', 'Norway', 'Poland', 'Portugal', 'Spain', 'Sweden',
'Switzerland', 'UK'],
'America': ['Argentina', 'Brazil', 'Canada', 'Mexico', 'USA', 'Venezuela'] }
print(df.columns)

#Crear un diccionario inverso para mapear país -> continente
mapa_paises = {country: continente for continente, countries in continentes.items() for country in countries}

#Asignar continente a cada fila del DataFrame
df['continente'] = df['country'].map(mapa_paises).fillna('Otro')

#Agrupar por continente y sumar pedidos
df_continente = df.groupby('country', as_index=False)['total_pedidos'].sum()


__Intento NO usar una QUERY ya que el ejercicio indica que no es necesario -->


'''

orders = pd.read_sql("SELECT order_id, customer_id FROM orders", conn)
customers = pd.read_sql("SELECT customer_id, country FROM customers", conn)

continentes = {
    'Europe': ['Austria', 'Belgium', 'Denmark', 'Finland', 'France',
               'Germany', 'Ireland', 'Italy', 'Norway', 'Poland', 
               'Portugal', 'Spain', 'Sweden', 'Switzerland', 'UK'],
    'America': ['Argentina', 'Brazil', 'Canada', 'Mexico', 'USA', 'Venezuela']
}

# Diccionario inverso para mapear país -> continente
mapa_paises = {pais: continente for continente, paises in continentes.items() for pais in paises}

# Unir tablas para obtener país de cada pedido
df_merged = orders.merge(customers, on='customer_id')

# Asignar continente a cada pedido antes de agrupar
df_merged['continente'] = df_merged['country'].map(mapa_paises).fillna('Otro')

# Contar pedidos por país y continente
df_pedidos = df_merged.groupby(['country', 'continente'], as_index=False)['order_id'].count()
df_pedidos = df_pedidos.rename(columns={'order_id': 'total_pedidos'})

# Ordenar por total_pedidos en orden descendente
df_pedidos = df_pedidos.sort_values(by='total_pedidos', ascending=False)

# Mostrar resultados ordenados
print(df_pedidos.head())

fig = px.pie(df_pedidos, 
             names='country', 
             values='total_pedidos', 
             title="Distribución de Pedidos por País")
fig.show()



## Pedidos con retraso














## Distribución media del precio

query12 = '''
SELECT 
    o.ship_country, 
    AVG(order_totals.total_price) AS avg_order_price
FROM Orders o
JOIN (
    -- Step 1: Compute the total order price per order
    SELECT 
        order_id, 
        SUM(unit_price * quantity * (1 - discount)) AS total_price
    FROM Order_details
    GROUP BY order_id
) order_totals ON o.order_id = order_totals.order_id
-- Step 2: Compute the average order total per country
GROUP BY o.ship_country;
'''

df = pd.read_sql(query12, conn)

plt.figure(figsize=(10, 6))
sns.barplot(x="ship_country", y="avg_order_price", data=df)

plt.xlabel("País de Envío")
plt.ylabel("Precio Medio del Pedido ($)")
plt.title("Distribución Media del Precio de Pedido por País")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()


## Clientes que no han pedido nunca

query13 = '''
SELECT 
    (SELECT COUNT(*) FROM Customers) AS total_clientes,
    COUNT(c.customer_id) AS clientes_sin_pedidos,
    ROUND((COUNT(c.customer_id) * 100.0) / (SELECT COUNT(*) FROM Customers), 2) AS porcentaje_sin_pedidos
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
'''
df = pd.read_sql(query13, con=engine)


## Productos más demandados

query14 = """
SELECT 
    p.product_name,
    p.units_in_stock,
    COALESCE(COUNT(od.order_id), 0) AS cantidad_vendida
FROM products p
LEFT JOIN order_details od ON p.product_id = od.product_id
GROUP BY p.product_name, p.units_in_stock
HAVING p.units_in_stock < 20
ORDER BY cantidad_vendida DESC;
"""
df = pd.read_sql(query14, con=engine)

plt.figure(figsize=(10, 6))
plt.barh(df["product_name"], df["cantidad_vendida"], color="skyblue")
plt.xlabel("Cantidad Vendida")
plt.ylabel("Producto")
plt.title("Productos con Menos de 20 Unidades en Stock y Cantidad Vendida")
plt.gca().invert_yaxis()  # Invierte el eje Y para que el más vendido esté arriba
plt.show()


##### EJERCICIO 4 #####

## Última vez que se pidió un producto
query15 = '''
SELECT 
    c.category_name,
    MAX(o.order_date) AS ultima_fecha_pedido
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN order_details od ON p.product_id = od.product_id
JOIN orders o ON od.order_id = o.order_id
GROUP BY c.category_name
ORDER BY ultima_fecha_pedido DESC;
'''
df = pd.read_sql(query15, con=engine)

## Productos nunca vedidos por su precio original

query16 = '''
SELECT 
    p.product_id,
    p.product_name
FROM products p
JOIN order_details od ON p.product_id = od.product_id
GROUP BY p.product_id, p.product_name
HAVING MIN(od.discount) > 0  
'''

#MIN(od.discount) > 0 : Nos dice cuál es el menor descuento que ha tenido un producto en 
# todas sus ventas. Si el menor descuento sigue siendo mayor que 0 (> 0), significa 
# que nunca se vendió sin descuento, es decir, nunca se vendió al precio original.

df = pd.read_sql(query16, con=engine)

## Identificar un producto

query17 = '''
SELECT 
    p.product_id, 
    p.product_name, 
    p.category_id
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE c.category_name = 'Confections';
'''
df = pd.read_sql(query17, con=engine)




## Proveedor con TODOS los productos descontinuados

query18 = '''
SELECT 
    s.supplier_id, 
    s.company_name
FROM suppliers s
JOIN products p ON s.supplier_id = p.supplier_id
GROUP BY s.supplier_id, s.company_name
HAVING MAX(p.discontinued) = 1 AND MIN(p.discontinued) = 1;
'''
df = pd.read_sql(query18, con=engine)
#El único proveedor es "Refrescos Americanas LTDA", Id 10.





## Clientes que compraron CHAI

query19 = '''
SELECT 
    c.customer_id,
    c.company_name,
	od.quantity
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_details od ON o.order_id = od.order_id
JOIN products p ON od.product_id = p.product_id
WHERE p.product_name = 'Chai'
AND od.quantity > 30;
'''
df = pd.read_sql(query19, con=engine)
# Resultado:
"Lehmanns Marktstand" 
"Berglunds snabbköp"
"LINO-Delicateses"
"Save-a-lot Markets"
"Seven Seas Imports"
"Bottom-Dollar Markets"
"Save-a-lot Markets"
"Lehmanns Marktstand"




## Clientes con suma de carga mayor de 1000

query20 = '''
SELECT 
    o.customer_id,
    c.company_name,
    SUM(od.quantity) AS total_carga
FROM orders o
JOIN order_details od ON o.order_id = od.order_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY o.customer_id, c.company_name
HAVING SUM(od.quantity) > 1000;
'''
df = pd.read_sql(query20, con=engine)
#Resultado:
"HILARION-Abastos"
"Rattlesnake Canyon Grocery"
"Queen Cozinha"
"Berglunds snabbköp"
"QUICK-Stop"
"Ernst Handel"
"Save-a-lot Markets"
"Frankenversand"
"Folk och fä HB"
"Suprêmes délices"
"White Clover Markets"
"Hungry Owl All-Night Grocers"


## Ciudades con más de 5 empleados

query21 = '''
SELECT city, COUNT(employee_id) AS total_empleados
FROM employees
GROUP BY city
HAVING COUNT(employee_id) > 5;
'''
df = pd.read_sql(query21, con=engine)
#No hay ninguna ciudad con más de 5 empleados







conn.close()






