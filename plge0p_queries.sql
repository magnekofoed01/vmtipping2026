-- Uttrekk 1: Kunder med Y40 som gikk til fornyelse (F) siste måned
WITH fornyelser AS (
    SELECT 
        E0KUND,
        E0OBJ,
        E0PAKK,
        E0STAT,
        E0TARA,
        E0TARM,
        E0TARD,
        E0TIDP,
        (E0TARA * 10000 + E0TARM * 100 + E0TARD) AS dato_int
    FROM SBT1DTA.PLGE0P
    WHERE E0OBJ = 'Y40'
      AND E0PAKK IN ('1MF', '1RT')
      AND E0STAT = 'F'
)
SELECT 
    E0KUND,
    E0OBJ,
    E0PAKK,
    E0STAT,
    E0TARA,
    E0TARM,
    E0TARD,
    E0TIDP
FROM fornyelser
WHERE dato_int >= (YEAR(CURRENT_DATE - 1 MONTH) * 10000 + MONTH(CURRENT_DATE - 1 MONTH) * 100 + DAY(CURRENT_DATE - 1 MONTH))
ORDER BY E0KUND, E0TARA DESC, E0TARM DESC, E0TARD DESC;

-- Uttrekk 2: Sjekk om samme kunder nå har Y51 eller Y52
WITH fornyelser AS (
    SELECT 
        E0KUND,
        E0OBJ,
        E0PAKK,
        E0STAT,
        E0TARA,
        E0TARM,
        E0TARD,
        (E0TARA * 10000 + E0TARM * 100 + E0TARD) AS dato_int
    FROM SBT1DTA.PLGE0P
    WHERE E0OBJ = 'Y40'
      AND E0PAKK IN ('1MF', '1RT')
      AND E0STAT = 'F'
),
nye_produkter AS (
    SELECT 
        E0KUND,
        E0OBJ,
        E0PAKK,
        E0STAT,
        E0TARA,
        E0TARM,
        E0TARD
    FROM SBT1DTA.PLGE0P
    WHERE E0OBJ IN ('Y51', 'Y52')
)
SELECT DISTINCT
    f.E0KUND,
    f.E0OBJ as GAMMELT_OBJ,
    f.E0PAKK as GAMMEL_PAKK,
    f.E0TARA as FORNYELSE_AAR,
    f.E0TARM as FORNYELSE_MND,
    f.E0TARD as FORNYELSE_DAG,
    n.E0OBJ as NYTT_OBJ,
    n.E0PAKK as NY_PAKK,
    n.E0TARA as NY_AAR,
    n.E0TARM as NY_MND,
    n.E0TARD as NY_DAG,
    n.E0STAT as NY_STATUS
FROM fornyelser f
INNER JOIN nye_produkter n ON f.E0KUND = n.E0KUND
WHERE f.dato_int >= (YEAR(CURRENT_DATE - 1 MONTH) * 10000 + MONTH(CURRENT_DATE - 1 MONTH) * 100 + DAY(CURRENT_DATE - 1 MONTH))
ORDER BY f.E0KUND, f.E0TARA DESC, f.E0TARM DESC, f.E0TARD DESC;

-- Uttrekk 3: Sammenligning - hvilke kunder har IKKE gått over til Y51/Y52
WITH fornyelser AS (
    SELECT 
        E0KUND,
        E0OBJ,
        E0PAKK,
        E0STAT,
        E0TARA,
        E0TARM,
        E0TARD,
        (E0TARA * 10000 + E0TARM * 100 + E0TARD) AS dato_int
    FROM SBT1DTA.PLGE0P
    WHERE E0OBJ = 'Y40'
      AND E0PAKK IN ('1MF', '1RT')
      AND E0STAT = 'F'
),
nye_produkter AS (
    SELECT DISTINCT E0KUND
    FROM SBT1DTA.PLGE0P
    WHERE E0OBJ IN ('Y51', 'Y52')
)
SELECT DISTINCT
    f.E0KUND,
    f.E0OBJ,
    f.E0PAKK,
    f.E0TARA as FORNYELSE_AAR,
    f.E0TARM as FORNYELSE_MND,
    f.E0TARD as FORNYELSE_DAG,
    f.E0STAT
FROM fornyelser f
WHERE f.dato_int >= (YEAR(CURRENT_DATE - 1 MONTH) * 10000 + MONTH(CURRENT_DATE - 1 MONTH) * 100 + DAY(CURRENT_DATE - 1 MONTH))
  AND f.E0KUND NOT IN (SELECT E0KUND FROM nye_produkter)
ORDER BY f.E0KUND;
