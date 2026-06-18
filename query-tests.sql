print('______________________________________')
print('HOW TO USE THIS TEST?')
print('')
print('Run this on a database.')
print('Switch your query window to write in text format (CTRL+T).')
print('Compare the expected results (printed on the screen) to the returned results manually. Takes 2 minutes.')
print('Switch back to grid view (CTRL+D).')
print('')
print('Update this file if the results are different, because:')
print('- a query changed/added/deleted')
print('- the database changed')
print('______________________________________')
print('')
print('')
print('______________________________________')
print('##sequel-basicland')
print('###basic-querying')
print('______________________________________')
print('')

print('Expected: 50 rows.')

SELECT * FROM person WHERE hair = 'Black'

print('___________________')

print('Expected: 79 rows.')

SELECT * FROM person WHERE is_male=1

print('___________________')

print('Expected: 24 rows.')

SELECT * FROM person
WHERE is_male=1 AND hair='Black'

print('___________________')

print('Expected 1 person: Neil Davis.')

SELECT * FROM person
WHERE is_male=1 AND hair='Black' AND shoe_size = 45

print('______________________________________')
print('##sequel-basicland')
print('###querying-with-tricky-types')
print('______________________________________')
print('')

print('Expected: 24 rows.')

print('Solution (simple):')

SELECT *, DATEDIFF(year, date_of_birth, GETDATE()) AS age 
FROM person 
WHERE DATEDIFF(year, date_of_birth, GETDATE()) >= 20 AND DATEDIFF(year, date_of_birth, GETDATE()) <= 30
ORDER BY age
 
print('Alternative solution (effective):');

WITH persons_with_age (first_name, last_name, age) AS (
       SELECT first_name, last_name, DATEDIFF(year, date_of_birth, GETDATE())
       FROM person
)
SELECT * FROM persons_with_age WHERE age >= 20 AND age <= 30
ORDER BY age;

print('___________________')

print('0 row expected')

SELECT *, DATEDIFF(year, date_of_birth, GETDATE()) AS age FROM person WHERE is_male=1 AND hair='Black' AND shoe_size = 45 AND DATEDIFF(year, date_of_birth, GETDATE()) >= 20 AND DATEDIFF(year, date_of_birth, GETDATE()) < 30;

print('___________________')

print('Expected: Martin Walsh')

SELECT *, DATEDIFF(year, date_of_birth, GETDATE()) AS age FROM person WHERE is_male=1 AND (hair='Black' OR hair IS NULL) AND shoe_size = 45 AND DATEDIFF(year, date_of_birth, GETDATE()) >= 20 AND DATEDIFF(year, date_of_birth, GETDATE()) < 30;

print('______________________________________')
print('##sequel-basicland')
print('###data-modification')
print('______________________________________')
print('')

print('Expected 1 row.')

SELECT * FROM person
WHERE first_name = 'Kira' AND last_name = 'Murray'

print('___________________')

print('Expected 2 rows: Hans Klein with person_id=398E6049-79CB-5B4E-9B36-E8C685E8543B and Cindy Klein with person_id=73CFED84-EEF9-864F-BBC2-51D1A1C0B897.')

SELECT * FROM person
WHERE (first_name = 'Hans'
OR first_name = 'Cindy') AND last_name = 'Klein'

print('______________________________________')
print('##midtown-join-and-aggregation')
print('###aggregation')
print('______________________________________')
print('')

print('Expected: The bank account of our victim: US48BANK830816901')

SELECT * FROM person p
JOIN account_person ap ON ap.person_id = p.person_id
JOIN account a ON a.iban = ap.iban
WHERE p.first_name = 'Vern' AND p.last_name = 'Jameson'

print('An equivalent solution:')

SELECT * FROM account_person ap 
JOIN person p ON p.person_id = ap.person_id
JOIN account a ON a.IBAN = ap.IBAN
WHERE last_name='Jameson' AND first_name='Vern'

print('___________________')

print('Expected: There were 15 contra party sending money to US48BANK830816901.')
print('  The contra account that transferred the most is US81BANK2096431873.')

SELECT contra_IBAN, SUM(amount) AS SUM
  FROM transfer
  WHERE IBAN = 'US48BANK830816901'
  GROUP BY contra_IBAN
  ORDER BY SUM DESC

print('___________________')

print('Expected: Peter Patrelli')

SELECT * FROM account_person AS ap
JOIN person AS p ON ap.person_id = p.person_id
WHERE ap.IBAN = 'US81BANK2096431873'

print('______________________________________')
print('##midtown-join-and-aggregation')
print('###complex-joins')
print('______________________________________')
print('')

print('Expected: a Sony hit included in a short list')

SELECT *
FROM phone AS ph 
JOIN person AS p ON p.person_id = ph.person_id
WHERE p.first_name = 'Peter' AND p.last_name='Patrelli'

print('___________________')

print('Expected: Ellie Burgess')

SELECT TOP 1 c.time, c.to_phone_number, c.from_phone_number, from_person.first_name, from_person.last_name, to_person.first_name, to_person.last_name
FROM call AS c
JOIN phone AS fph ON fph.phone_number = c.from_phone_number
JOIN phone AS tph ON tph.phone_number = c.to_phone_number
JOIN person AS from_person ON from_person.person_id = fph.person_id
JOIN person AS to_person ON to_person.person_id = tph.person_id
WHERE to_person.first_name = 'Peter' AND to_person.last_name='Patrelli'
AND tph.make = 'Sony'
ORDER BY time DESC

print('______________________________________')
print('##midtown-join-and-aggregation')
print('###simple-joins')
print('______________________________________')
print('')

print('Expected: 1 hit')

SELECT p.first_name, p.last_name, c.color, c.make, c.model, c.license_plate
FROM person AS p
JOIN car AS c ON p.person_id = c.person_id
WHERE make = 'Mercedes' and color = 'blue';

print('___________________')

print('Expected: 0 result.')

SELECT p.first_name, p.last_name, c.color, c.make, c.model, c.license_plate 
FROM person AS p
JOIN car AS c ON p.person_id = c.person_id
WHERE make='Mercedes' AND color = 'blue' AND license_plate LIKE '66%'

print('___________________')

print('Expected: a C-class Mercedes with license plate 66-B4-79 but without an owner.')

SELECT p.first_name, p.last_name, c.color, c.make, c.model, c.license_plate FROM person AS p
RIGHT JOIN car AS c ON p.person_id = c.person_id
WHERE color = 'blue' AND license_plate LIKE '66%'

print('___________________')
print('Expected: there are hits')

SELECT * 
FROM transfer 
WHERE description = 'Car rental 66-B4-79'

print('___________________')
print('Expected: exactly 1 hit')

SELECT TOP 1 t.*, p.first_name, p.last_name 
FROM transfer t 
JOIN account_person ap ON t.IBAN = ap.IBAN 
JOIN person p ON ap.person_id = p.person_id 
WHERE t.description = 'Car rental 66-B4-79' 
ORDER BY DATE DESC


print('______________________________________')
print('##javapark')
print('###jooq')
print('###jpa')
print('###plain-jdbc')

print('##locks')
print('###defeat-the-deadlock')
print('______________________________________')
print('')

print('Expected: exactly 1 hit')

select * from account where iban = 'US12BANK439875439'

print('______________________________________')
print('HOW TO USE THIS TEST?')
print('')
print('Run this on a database.')
print('Switch your query window to write in text format (CTRL+T).')
print('Compare the expected results (printed on the screen) to the returned results manually. Takes 2 minutes.')
print('Switch back to grid view (CTRL+D).')
print('')
print('Update this file if the results are different, because:')
print('- a query changed/added/deleted')
print('- the database changed')
print('______________________________________')
