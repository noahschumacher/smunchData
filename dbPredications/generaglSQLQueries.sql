-- Get all company names ordered in the past 2 months
SELECT DISTINCT name FROM companies
-- Get nunmber of companies ordere in past 2 months
SELECT COUNT(DISTINCT name) FROM companies

-- # of companies that ordered <30 days AND >30 days ago
(SELECT DISTINCT(company_email_domain) FROM
	(
		SELECT split_part(U.email, '@', 2)  FROM
			users U INNER JOIN choices C ON U.id = C.user_id WHERE C.closed_at < NOW() - interval '60 days'
	) AS company_email_domain
) AS CED2 ON CED.company_email_domain = CED2.company_email_domain


SELECT CED.company_email_domain FROM
	(
		SELECT DISTINCT(company_email_domain) FROM
		(
			SELECT split_part(U.email, '@', 2)  FROM
				users U INNER JOIN choices C ON U.id = C.user_id WHERE C.closed_at > NOW() - interval '30 days'
		) AS company_email_domain 
	) AS CED INNER JOIN
	(
		SELECT DISTINCT(company_email_domain) FROM
		(
			SELECT split_part(U.email, '@', 2)  FROM
				users U INNER JOIN choices C ON U.id = C.user_id WHERE C.closed_at < NOW() - interval '30 days'
		) AS company_email_domain 
	) AS CED2 ON CED.company_email_domain = CED2.company_email_domain
	
-- Gets all the Restraunt names
SELECT DISTINCT name FROM restaurants
-- Get number of all restraunts
SELECT COUNT(DISTINCT name) from restaurants

-- Get orders from company A on day B


-- Get orders from company A from restaurant B


