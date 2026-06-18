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
print('##performance-bay')
print('###execution-plan')
print('______________________________________')
print('')

print('Expected: ~1M lines')

SELECT COUNT(*) FROM call -- ~1M lines

print('Expected: ~200 lines')

SELECT COUNT(*) FROM phone -- ~200 lines

print('Expected: ~160 lines')

SELECT COUNT(*) FROM person -- ~160 lines

print('___________________')
print('Expected: 2 lines: one for the clustered index, one for the PK')

SELECT * 
FROM sys.indexes 
WHERE object_id = OBJECT_ID('dbo.call')

print('___________________')

print('Expected: ~886 lines')

SELECT p.first_name + ' ' + p.last_name, c.from_phone_number, c.to_phone_number, 
	SUM(c.duration_sec) sum_duration_sec, SUM(c.duration_sec)/60/60 sum_duration_hour
FROM call c
JOIN phone ph ON (ph.phone_number = c.from_phone_number)
JOIN person p ON (p.person_id = ph.person_id)
GROUP BY c.from_phone_number, c.to_phone_number, p.first_name, p.last_name
ORDER BY sum_duration_sec DESC

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
