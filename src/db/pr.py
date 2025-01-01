import logger
from db.db import DB

# 
log = logger.getLogger("pr")
class Pr(DB):
    def __init__(self, file):
        super().__init__(file)
        # Create the pr_details table with a foreign key reference to the users table
        success = self.create('''
            CREATE TABLE IF NOT EXISTS pr_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            pr TEXT NOT NULL,
            trigger TEXT NOT NULL,
            FOREIGN KEY (email) REFERENCES users(userId)
            )
            ''')
        log.info(f"result of create {success}") 



    def insert_pr_details(self, email, pr, trigger):
        """
        Inserts pull request details into the database.

        Args:
            email (str): The email associated with the pull request.
            pr (str): The pull request identifier or details.
            trigger (str): The trigger event or condition for the pull request.

        Returns:
            None
        """
        cursor = self.execute_with_data('''
        INSERT INTO pr_details (email, pr, trigger) VALUES (?, ?, ?)
        ''', (email, pr, trigger))
        if cursor.rowcount == 0:
                log.warning(f"No entry found for email: {email} and pr: {pr}")
        self.conn.commit()
          
          
            
    def query_pr_details_by_email(self, email):
        """
        Query pull request details by email.

        This method executes a SQL query to fetch pull request details and triggers
        from the 'pr_details' table where the email matches the provided email pattern.

        Args:
            email (str): The email address to search for in the 'pr_details' table.

        Returns:
            list: A list of tuples containing the pull request details and triggers
                  that match the provided email pattern.
        """
        cursor = self.execute_with_data('''
        SELECT pr, trigger FROM pr_details WHERE email LIKE ?
        ''', ('%' + email + '%',))
        return cursor.fetchall()


    
    def query_by_email(self, email):
        """
        Query the database for records in the 'pr_details' table where the email field matches the given email pattern.

        Args:
            email (str): The email pattern to search for in the 'pr_details' table.

        Returns:
            list: A list of tuples containing the rows that match the email pattern.
        """
        cursor = self.execute_with_data('''
        SELECT * FROM pr_details WHERE email LIKE ?
        ''', ('%' + email + '%',))
        return cursor.fetchall()
    
    
    
    def query_emails_by_pr_and_triggers(self, pr, trigger):
        """
        Query the database for emails that have the same 'pr' as the first parameter
        and 'trigger' set to 'all' or 'trigger' set to 'succeed' but the second parameter shall be 'blue'.

        Args:
            pr (str): The pull request identifier or details.
            trigger (str): The trigger event or condition for the pull request.

        Returns:
            list: A list of emails that match the criteria.
        """
        cursor = self.execute_with_data('''
        SELECT email FROM pr_details 
        WHERE pr = ? AND ((trigger = 'all' OR trigger = 'merged') OR (trigger = 'succeed' AND ? = 'blue'))
        ''', (pr, trigger))
        return [row[0] for row in cursor.fetchall()]



    def remove_pr_details_by_email_and_prs(self, email, prs):
        """
        Remove all entries from the 'pr_details' table that match the given email 
        and any of the prs in the list.

        Args:
            email (str): The email associated with the pull requests.
            prs (list): A list of pull request identifiers or details.

        Returns:
            None
        """
        for pr in prs:
            self.remove_pr_details_by_email_and_pr(email, pr)



    def remove_pr_details_by_email_and_pr(self, email, pr):
        """
        Remove all entries from the 'pr_details' table that match the given email 
        and any of the prs in the list.

        Args:
            email (str): The email associated with the pull requests.
            prs (list): A list of pull request identifiers or details.

        Returns:
            None
        """
        cursor = self.execute_with_data('''
        DELETE FROM pr_details WHERE email = ? AND pr = ?
        ''', (email, pr))
        if cursor.rowcount == 0:
            log.warning(f"No entry found for email: {email} and pr: {pr}")
        self.conn.commit()

    def get_all_prs_and_emails(self):
        """
        Retrieve all pull requests and their associated emails from the 'pr_details' table.

        Returns:
            list: A list of tuples containing the email and pull request details.
        """
        cursor = self.execute('''
        SELECT email, pr FROM pr_details
        ''')
        return cursor.fetchall()