import time

from locust import HttpUser, task, between



class QuickstartUser(HttpUser):

    wait_time = between(1, 2)



    @task(2)

    def news_page(self):

        self.client.get("/news")



    @task(2)

    def news_detail(self):

        self.client.get("/news/detail/1b637852-232e-11eb-b929-506b8d923f0f")



    @task(2)

    def agenda_page(self):

        self.client.get("/agenda")
		


    @task(1)

    def rss_page(self):

        self.client.get("/rss-news/list")


    @task(1)

    def rss_detail(self):

        self.client.get("/rss-news/detail/0ed552ac-224f-11eb-aa17-00059a3c7a00")


		
    @task(2)

    def employee_page(self):

        self.client.get("/employee")

		
		
    @task(1)

    def hr_event_page(self):

        self.client.get("/hr-event")
		
		
		
    @task(2)

    def announcement_page(self):

        self.client.get("/announcement")	
		
	
	
    @task(3)

    def sop_page(self):

        self.client.get("/general-content/sop")	

		
		
    @task(3)

    def sop_detail(self):

        self.client.get("/document-viewer/general-content/sop/df785c56-2006-11eb-aa70-506b8d923f0f")		
		
		
		
    @task(3)

    def form_page(self):

        self.client.get("/document-viewer/general-content/sop/df785c56-2006-11eb-aa70-506b8d923f0f")	

		
		
    @task(1)

    def ehs_page(self):

        self.client.get("/ehs-statistic")	

		
		
    @task(1)

    def simpul_page(self):

        self.client.get("/general-content/simpul")			
		
		
		
    @task(1)

    def simpul_detail(self):

        self.client.get("/document-viewer/general-content/simpul/2d32c048-1a90-11eb-bc84-506b8d923f0f")
		
		

	@task(1)

    def ecakrawala_page(self):

        self.client.get("/general-content/e-cakrawala")			
		
		
		
	@task(1)

    def ecakrawala_detail(self):

        self.client.get("/document-viewer/general-content/e-cakrawala/6bd719ee-1e81-11eb-bc79-506b8d923f0f")		


		
	@task(1)

    def info_employee(self):

        self.client.get("/employee-info")		
			
		
		
    def on_start(self):

        self.client.get("/")



