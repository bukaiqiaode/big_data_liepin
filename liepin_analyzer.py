# -*- coding:utf-8 -*-

class liepin_anar(object):
    def __init__(self, arr_content):
        '''
        str_content: content retrieved from web
        '''
        self.raw_data = []
        for item in arr_content:
            #replace "\\n"
            item = item.replace('\\n', '')
            #trim the spaces
            item = item.strip()

            if len(item) > 0:
                self.raw_data.append(item)            

        self.job_title = ""
        self.company_info = ""
        self.company_link = ""
        
        #announced sallary from the company
        self.budget = ""
        self.publish_time = ""

        self.qualifications = []
        self.tag_list = []
        self.job_description = ""
        
    def process(self):
        length = len(self.raw_data)
        indexer = 0
        
        while indexer < length:
            item = self.raw_data[indexer]
            #replace "\\n"
            item = item.replace('\\n', '')
            #trim the spaces
            item = item.strip()

            if item == "<div class=\"title-info\">":
                while self.raw_data[indexer] != "</h3>":
                    if self.raw_data[indexer].startswith("<h1"):
                        self.job_title = self.raw_data[indexer]
                    elif self.raw_data[indexer].startswith("<a"):
                        self.company_info = self.raw_data[indexer]
                    indexer = indexer + 1
            elif item.startswith("<p class=\"job-item-title\">"):
                self.budget = self.raw_data[indexer]
            elif item.startswith("<time"):
                self.publish_time = self.raw_data[indexer]
            elif item == "<div class=\"job-qualifications\">":
                self.qualifications.append(self.raw_data[indexer + 1])
                self.qualifications.append(self.raw_data[indexer + 2])
                indexer = indexer + 3
            elif item == "<div class=\"tag-list\">":
                indexer = indexer + 1
                while self.raw_data[indexer] != "</div>":
                    self.tag_list.append(self.raw_data[indexer])
                    indexer += 1
            elif item.startswith("<div class=\"content content-word\">"):
                self.job_description = (self.raw_data[indexer])
                indexer += 4
                '''
                while self.raw_data[indexer] != "<!-- 其他信息 -->":
                    self.job_description.append(self.raw_data[indexer])
                    indexer += 1
                '''
            indexer += 1

        tmp = self.job_title.index("\"")
        self.job_title = self.job_title[tmp + 1:]
        tmp = self.job_title.index("\"")
        self.job_title = self.job_title[:tmp]

        self.budget = self.budget.replace("<p class=\"job-item-title\">", '')        

        tmp = self.publish_time.index("\"")
        self.publish_time = self.publish_time[tmp + 1:]
        tmp = self.publish_time.index("\"")
        self.publish_time = self.publish_time[:tmp]

        tmp = self.company_info.index("\"")
        self.company_info = self.company_info[tmp + 1:]
        tmp = self.company_info.index("\"")
        self.company_link = self.company_info[0:tmp]
        
        tmp = self.company_info.index('>')
        self.company_info = self.company_info[tmp + 1:-4]

        length = len(self.qualifications)
        indexer = 0
        arr_tmp = []
        while indexer < length:
            tmp = self.qualifications[indexer].strip()
            tmp = tmp.replace("<span>", '')
            tmp = tmp.replace("</span>", ',')
            tmp = tmp.replace('\n', '').strip().split(',')
            for item in tmp:
                item = item.strip()
                if item != "," and item != '\n' and item != '':
                    arr_tmp.append(item)                    
            indexer += 1
        self.qualifications = arr_tmp

        length = len(self.tag_list)
        indexer = 0
        while indexer < length:
            tmp_1 = self.tag_list[indexer].index('>')
            tmp_2 = self.tag_list[indexer].index("</span>")
            self.tag_list[indexer] = self.tag_list[indexer][tmp_1 + 1:tmp_2]
            indexer += 1
            
        self.job_description = self.job_description.replace("<div class=\"content content-word\">", '')
        return

    def sayit(self):
        print "\n*************************"
        print "job_title:"
        print self.job_title.decode('utf-8')
        print "company_info:"
        print self.company_info.decode('utf-8')
        print "company_link:"
        print self.company_link.decode('utf-8')
        print "budget:"
        print self.budget.decode('utf-8')
        print "publish_time:"
        print self.publish_time.decode('utf-8')

        print "qualifications:"
        self.print_qualifications()
        print "tags:"        
        self.print_tag_list()
        print "description:"
        self.print_job_description()

    def print_qualifications(self):
        for item in self.qualifications:
            print item.decode('utf-8')
    def print_tag_list(self):
        for item in self.tag_list:
            print item.decode('utf-8')
    def print_job_description(self):
        print self.job_description.replace("<br/>", '\n').decode('utf-8')

    def valid(self):
        ret_val = True
        if len(self.job_title) == 0:
            ret_val = False
        if len(self.company_info) == 0:
            ret_val = False
        if len(self.company_link) == 0:
            ret_val = False
        if len(self.budget) == 0:
            ret_val = False
        if len(self.publish_time) == 0:
            ret_val = False
        if len(self.qualifications) == 0:
            ret_val = False
        if len(self.tag_list) == 0:
            ret_val = False
        if len(self.job_description) == 0:
            ret_val = False
        return ret_val
