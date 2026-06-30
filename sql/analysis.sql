SELECT country, SUM(consumption) AS total_consumption
FROM coffee_data
GROUP BY country
ORDER BY total_consumption DESC;

SELECT year, SUM(consumption) AS total_consumption
FROM coffee_data
GROUP BY year
ORDER BY year;

CREATE TABLE market_analysis AS
SELECT 
    country,
    SUM(consumption) AS total_consumption,
    AVG(population) AS avg_population,
    AVG(coffee_per_capita) AS per_capita
FROM coffee_data
GROUP BY country;
``
