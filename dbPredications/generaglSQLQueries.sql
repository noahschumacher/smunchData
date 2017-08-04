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



SELECT ( 
	DISTINCT companies.name, closings.company_id
	FROM (
		closings
		INNER JOIN (
			companies ON closings.company_id = companies.id
			WHERE (
				closings.delivered_at > CURRENT_DATE - interval '60 days'
				)
			)
		)
	)

for company_id in companies:
	for delivered_at in deliverys_dates:
SELECT choices.user_id, choices.company_delivery_id, choices.updated_at, closings.choice_id, closings.delivered_at, closings.dish_count
	FROM closings
		INNER JOIN choices ON closings.choice_id = choices.id
			WHERE choices.menue_dish_id IS NOT null AND 
				closings.company_id = %s AND 
				closings.delivered_at = %s %(company_id, delivered_at...)


Staff.find_by_sql(<<-SQL
        SELECT *,
            icount( needed_ids ) as needcount,
            icount( optional_ids ) as optcount
          FROM (
            SELECT *,
              skillids & ARRAY#{ job.needed_skills.map(&:id) }::int[] AS needed_ids,
              skillids & ARRAY#{ job.optional_skills.map(&:id) }::int[] AS optional_ids
            FROM (
              SELECT DISTINCT
                "staffs"."id" as id,
                "staffs"."phone" as phone,
                "staffs"."fsm_state" as fsm_state,
                "staffs"."work_radius" as work_radius,
                "staffs"."profile_status" as profile_status,
                "staffs"."latitude" as latitude,
                "staffs"."longitude" as longitude,
                "staffs"."employment_starts_on" as employment_starts_on,
                "staffs"."employment_ends_on" as employment_ends_on,
                #{ select_distance }
                array_replace( array_agg("skills"."id"), NULL, 0)::int[] as skillids
              FROM "staffs"
                LEFT OUTER JOIN "staff_skills"  ON "staff_skills"."staff_id" = "staffs"."id" 
                LEFT OUTER JOIN "skills"        ON "skills"."id" = "staff_skills"."skill_id" 
                JOIN "users"                    ON "users"."profession_id" = "staffs"."id" AND "users"."profession_type" = 'Staff'
              WHERE   #{ where_address } #{ where_active }
                      "users"."email" IS NOT NULL
              GROUP BY "staffs"."id"
            ) tx1 
            #{ 
              (where_distance.present? || where_qualified.present?) ? 'WHERE ' : '' 
            }#{ 
              where_distance 
            }#{ 
              (where_distance.present? && where_qualified.present?) ? ' AND ' : '' 
            }#{ 
              where_qualified 
            }
          ) tx2
          ORDER BY needcount DESC, optcount DESC#{ order_distance }
          LIMIT #{ limit }
        SQL
      )
-- Get orders from company A on day B


-- Get orders from company A from restaurant B


