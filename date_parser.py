#!/usr/bin/env python

"""
Module to parse input string and interpret/extract dates from it
"""
from natty import DateParser
from time import strptime
from datetime import datetime, timedelta, date
import re


class DateParsing:
    """
    Class to extract date / date ranges from a string
    """
    def __init__(self):
        """
        Constructor to load a dictionary of common time phrases
        """
        self.__load()

    def date_monday(self):
        """
        Method to return the date on last Monday. Used by many methods as a reference to
        calculate a date range eg. last week = last Monday to previous Monday
        :return date of last monday:
        """
        day_no = date.today().weekday()
        if day_no == 0:
            return date.today()
        else:
            return date.today() - timedelta(days=day_no)

    def __load(self):
        """
        Private method(using name mangling) containing dictionary of commonly used time
        phrases and the corresponding operations to obtain the dates
        """
        self.time_phrases_and_ops = {
            'previous day': "self.day_evaluation()",
            'yesterday': "self.day_evaluation()",
            'previous week': "self.week_evaluation()",
            'last week': "self.week_evaluation()",
            'fortnightly': "self.fortnight_evaluation()",
            'fortnight': "self.fortnight_evaluation()",
            "last two weeks": "self.fortnight_evaluation()",
            "past two weeks": "self.fortnight_evaluation()",
            'last month': "self.last_month_evaluation()",
            'previous month': "self.last_month_evaluation()",
            'previous quarter': "self.prior_quarter_evaluation()",
            'quarter prior to the this': "self.prior_quarter_evaluation()",
            'last quarter': "self.prior_quarter_evaluation()",
            'last year': "self.previous_year_evaluation()",
            'previous year': "self.previous_year_evaluation()",
            'current month': "self.this_mth_evaluation()",
            'ongoing month': "self.this_mth_evaluation()",
            "last three weeks": "self.three_week_evaluation()",
            "past three weeks": "self.three_week_evaluation()",
            "last four weeks" : "self.four_week_evaluation()",
            "past four weeks" : "self.four_week_evaluation()"
        }

    def this_mth_evaluation(self):
        """
        Method to obtain current month date range
        :return date value from 1st of ongoing month to current date:
        """
        return [(date(self.date_monday().year, self.date_monday().month, 1)).strftime("%Y-%m-%d")]

    def day_evaluation(self):
        """
        Method to obtain current date(= date on last Monday)
        :return current date(= date on last Monday):
        """
        return self.date_monday()

    def three_week_evaluation(self):
        """
        Method to obtain date range for past three weeks
        :return:
        """
        today = self.date_monday()
        start_date = today - timedelta(days=28)
        end_date = start_date + timedelta(days=21)
        return [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

    def four_week_evaluation(self):
        """
        Method to obtain date range for past four weeks
        :return:
        """
        today = self.date_monday()
        start_date = today - timedelta(days=35)
        end_date = start_date + timedelta(days=28)
        return [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

    def week_evaluation(self):
        """
        Method to obtain last week date range
        :return date range of previous week:
        """
        today = self.date_monday()
        start_date = today - timedelta(days=14)
        end_date = start_date + timedelta(days=7)
        return [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

    def fortnight_evaluation(self):
        """
        Method to obtain fortnight date range
        :return date range of last fortnight:
        """
        today = self.date_monday()
        start_date = today - timedelta(days=21)
        end_date = start_date + timedelta(days=14)
        return [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

    def last_month_evaluation(self):
        """
        Method to obtain last month date range
        :return last month date range:
        """
        return [(date.today().replace(day=1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d'),
                (date.today().replace(day=1) - timedelta(days=1)).strftime('%Y-%m-%d')]

    def prior_quarter_evaluation(self):
        """
        Method to obtain last quarter date range
        :return last quarter date range:
        """
        today = date.today()
        curr_quarter = (today.month - 1) / 3 + 1
        if curr_quarter == 1:
            start_date = date(today.year - 1, 10, 1)
            end_date = date(today.year - 1, 12, 1)
        else:
            start_date = date(today.year, 3 * (curr_quarter - 1) + 1, 1)
            end_date = date(today.year, 3 * (curr_quarter - 1) + 4, 1) + timedelta(days=-1)
        return [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

    def previous_year_evaluation(self):
        """
        Method to obtain last year date range
        :return last year date range:
        """
        today = date.today()
        start_date = date(today.year - 1, 1, 1)
        end_date = date(today.year - 1, 12, 31)
        return [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

    def only_year_parse(self, query):
        """
        Parse query for year related phrases and then extract/interpret the year number
        :param query:
        :return year / year range:
        """
        if "this year" in query or "current year" in query:
            return [date(date.today().year,1,1).strftime('%Y-%m-%d'), date(date.today().year,date.today().month,date.today().day).strftime('%Y-%m-%d')]
        only_year_regex1 = re.compile(r'(before|after|in|during|for the year|for|from)\s([0-9]{4})\b(?!after)', re.IGNORECASE)
        only_year_regex2 = re.compile(
            r'(from|between|before)\s([0-9]{4})(\s| to | and |-| and after | after )([0-9]{4})(?=\D|$)', re.IGNORECASE)
        m1 = only_year_regex1.search(query)
        m2 = only_year_regex2.search(query)
        if m1:
            captured_values1 = m1.groups()
        if m2:
            captured_values2 = m2.groups()

        if m1:
            if captured_values1[0] == 'before':
                return [date(1970,1,1).strftime('%Y-%m-%d'), date(int(captured_values1[1]), 1, 1).strftime('%Y-%m-%d')]
            elif captured_values1[0] == 'after':
                return [date(int(captured_values1[1]), 1, 1).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d')]
        elif m2:
            return [date(int(captured_values2[1]), 1, 1).strftime('%Y-%m-%d'),
                    date(int(captured_values2[3]), 12, 31).strftime('%Y-%m-%d')]
        if m1:
            return [date(int(captured_values1[1]), 1, 1).strftime('%Y-%m-%d'),
                    date(int(captured_values1[1]), 12, 31).strftime('%Y-%m-%d')]
        else:
            return None

    def check_before(self, query):
        """
        Parse query for mentions of date after the word 'before'
        :param query:
        :return date / date range:
        """
        if "up to" in query:
            temp = query[query.index("up to") + 6:]
        elif "upto" in query:
            temp = query[query.index("upto") + 5:]
        else:
            temp = query[query.index("before") + 7:]
        # dd[-/ .]mm[-/ .]yyyy
        dateformat1_regex = re.compile('[0-3]?[0-9]{1}[-/ .]{1}[0-1]?[0-9]{1}((-|/| |.){1}\d{4})?(\s|$)')
        # yyyy[-/ .]mm[-/ .]dd
        dateformat2_regex = re.compile('[0-9]{4}[-/ .]{1}[0-1]?[0-9]{1}[-/ .]{1}[0-3]?[0-9]{1}')

        if dateformat1_regex.search(temp):
            dt_mth_yr = dateformat1_regex.search(temp).group().strip().split('/')
            if len(dt_mth_yr) == 2:
                return ['1970-1-1', date(date.today().year, int(dt_mth_yr[1]), int(dt_mth_yr[0])).strftime('%Y-%m-%d')]
            else:
                return ['1970-1-1', date(int(dt_mth_yr[2]), int(dt_mth_yr[1]), int(dt_mth_yr[0])).strftime('%Y-%m-%d')]

        elif dateformat2_regex.search(temp):
            yr_mth_dt = dateformat2_regex.search(temp).group().strip().split('/')
            if len(yr_mth_dt) == 2:
                return ['1970-1-1', date(int(yr_mth_dt[0]), int(yr_mth_dt[1]), 1).strftime('%Y-%m-%d')]
            else:
                return ['1970-1-1', date(int(yr_mth_dt[0]), int(yr_mth_dt[1]), int(yr_mth_dt[2])).strftime('%Y-%m-%d')]
        else:
            dt = DateParser(temp).result()[0].strftime('%Y-%m-%d')
            # print dt, date.today().strftime('%Y-%m-%d')
            if dt is not None and dt != date.today().strftime('%Y-%m-%d'):
                return ['1970-1-1', dt]
            else:
                return None

    def check_after(self, query):
        """
        Parse query for mentions of date after the word 'after'
        :param query:
        :return date / date range:
        """
        temp = query[query.index("after") + 6:]
        # dd[-/ .]mm[-/ .]yyyy
        dateformat1_regex = re.compile('[0-3]?[0-9]{1}[-/ .]{1}[0-1]?[0-9]{1}((-|/| |.){1}\d{4})?(\s|$)')
        # yyyy[-/ .]mm[-/ .]dd
        dateformat2_regex = re.compile('[0-9]{4}[-/ .]{1}[0-1]?[0-9]{1}[-/ .]{1}[0-3]?[0-9]{1}')

        if dateformat1_regex.search(temp):
            dt_mth_yr = dateformat1_regex.search(temp).group().strip().split('/')
            if len(dt_mth_yr) == 2:
                return [date(date.today().year, int(dt_mth_yr[1]), int(dt_mth_yr[0])).strftime('%Y-%m-%d'),
                        date.today().strftime('%Y-%m-%d')]
            else:
                return [date(int(dt_mth_yr[2]), int(dt_mth_yr[1]), int(dt_mth_yr[0])).strftime('%Y-%m-%d'),
                        date.today().strftime('%Y-%m-%d')]

        elif dateformat2_regex.search(temp):
            yr_mth_dt = dateformat2_regex.search(temp).group().strip().split('/')
            # print "after", dateformat2_regex.search(temp).group()
            if len(yr_mth_dt) == 2:
                return [date(int(yr_mth_dt[0]), int(yr_mth_dt[1]), 1).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d')]
            else:
                return [date(int(yr_mth_dt[0]), int(yr_mth_dt[1]), int(yr_mth_dt[2])).strftime('%Y-%m-%d'),
                        date.today().strftime('%Y-%m-%d')]

        else:
            dt = DateParser(temp).result()[0].strftime('%Y-%m-%d')
            # print dt, date.today().strftime('%Y-%m-%d')
            if dt is not None and dt != date.today().strftime('%Y-%m-%d'):
                return [dt, date.today().strftime('%Y-%m-%d')]
            else:
                return None

    def only_month_capture(self, query):
        """
        Parse query for mentions of month after some pre-specified phrases
        :param query:
        :return:
        """
        regex_month = re.compile(
            r'(for|in|during|for the month of|for this|in the month of)'
            r'{1}\s(January|February|March|April|May|June|July|August|September|October|November|December)(\s|$)', re.IGNORECASE)
        regex_month_year = re.compile(r'(for|in|during|for the month of|for this)'
                                      r'{1}\s(January|February|March|April|May|June|July|August|September|October|November|December)'
                                      r'{1}\s([0-9]{4})', re.IGNORECASE)
        if "before" in query:
            temp = query[query.index("before") + 7:]
            return ['1970-1-1', DateParser(temp).result()[0].strftime('%Y-%m-%d')]
        elif "after" in query:
            temp = query[query.index("after") + 6:]
            return [DateParser(temp).result()[0].strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d')]
        elif regex_month_year.search(query):
            m = regex_month_year.search(query).groups()
            start_date = date(int(m[2]), strptime(m[1][:3], '%b').tm_mon, 1)
            end_date = date(int(m[2]), (strptime(m[1][:3], '%b').tm_mon) % 12 + 1, 1) - timedelta(days=1)
            return [str(start_date), str(end_date)]
        elif regex_month.search(query):
            m = regex_month.search(query).groups()
            start_date = date(date.today().year, strptime(m[1][:3], '%b').tm_mon, 1)
            end_date = date(date.today().year, (strptime(m[1][:3], '%b').tm_mon)%12+1, 1) - timedelta(days=1)
            return [str(start_date), str(end_date)]
        else:
            return None

    def n_month_capture(self, query):
        """
        Parse query for 'n month' type of phrases
        :return:
        """
        word_to_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
                       "nine": 9}
        regex_n_month = re.compile(r'(last|past|previous)\s([0-9]|one|two|three|four|five|six|seven|eight|nine)'
                                   r'\s(month|months)',
                                   re.IGNORECASE)
        if regex_n_month.search(query):
            n_mth = list(regex_n_month.search(query).groups())
            if n_mth[1] in word_to_num:
                n_mth[1] = word_to_num[n_mth[1]]
            start_date = (date.today() - timedelta(days=int(n_mth[1]) * 30)).replace(day=1)
            end_date = date.today() - timedelta(days=date.today().day)
            return [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

    def parse_date(self, query):
        """
        Main method that parses the date in a query using all the other methods
        :param query:
        :return date range(if any):
        """
        query = query.lower()
        # check if the query contains only year reference eg. show sales for 2013
        dates = self.only_year_parse(query)
        if dates is not None:
            return dates

        # check if query contains "before" or "after" references
        if "before" in query or "upto" in query or "up to" in query:
            dates = self.check_before(query)
            if dates:
                return dates
        if "after" in query:
            dates = self.check_after(query)
            if dates:
                return dates

        # parse query for a list of time phrases specified by time_phrases_and_ops
        for phrase, func in self.time_phrases_and_ops.items():
            if phrase in query:
                date_range = eval(func)
                if len(date_range) == 2 and date_range[0] > date_range[1]:
                    date_range[0], date_range[1] = date_range[1], date_range[0]
                return date_range

        # capture only months
        dates = self.only_month_capture(query)
        if dates:
            return dates

        # capture n months
        dates = self.n_month_capture(query)
        if dates:
            return dates

        # parse query using natty
        dp = DateParser(query)
        date_list = dp.result()
        dates = []
        if date_list is not None:
            for d in date_list:
                dates.append(d.strftime('%Y-%m-%d'))
            if len(set(dates)) == 1 and dates[0] == date.today().strftime('%Y-%m-%d'):
                if "this month" in query or "current month" in query or "ongoing month" in query:
                    return [date(date.today().year, date.today().month, 1).strftime('%Y-%m-%d'),
                            date.today().strftime('%Y-%m-%d')]
                else:
                    return None
            else:
                if len(dates)==2 and dates[0] > dates[1]:
                    dates[0], dates[1] = dates[1], dates[0]
                return dates
        else:
                return None