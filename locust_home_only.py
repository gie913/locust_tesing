import time

from locust import HttpUser, task, between



class QuickstartUser(HttpUser):

    wait_time = between(1, 2)


			
		
		
    def on_start(self):

        self.client.get("/")



    @task(1)

    def ehs_page(self):

        self.client.get("/ehs-statistic")
		
		

    @task(2)

    def news_page(self):

        self.client.get("/news")
		
	
	
    @task(1)

    def simpul_detail(self):

        self.client.get("/document-viewer/general-content/simpul/2d32c048-1a90-11eb-bc84-506b8d923f0f")
		
		
	@task(1)

    def rss_detail(self):

        self.client.get("/rss-news/detail/0ed552ac-224f-11eb-aa17-00059a3c7a00")


			
