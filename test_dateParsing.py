#!/usr/bin/env python
from unittest import TestCase
from datetime import date, timedelta
from date_parser import DateParsing


class TestDateParser(TestCase):

    def date_monday(self):
        """
        Method to return the date on last Monday. Used by many methods as a reference to
        calculate a date range eg. last week = last Monday to previous Monday
        :return date of last monday:
        """
        day_no = date.today().weekday()
        if day_no == 0:
            return date.today() - timedelta(days=7)
        else:
            return date.today() - timedelta(days=day_no+1+7)

    def test_parse_date(self):

        dt_parse = DateParsing()

        # self.assertEquals(dt_parse.parse_date("sales in last quarter"),

        self.assertEquals(dt_parse.parse_date("Sales in the past two days"),
                          [(date.today() - timedelta(days=2)).strftime("%Y-%m-%d"),
                           date.today().strftime("%Y-%m-%d")])

        self.assertEquals(dt_parse.parse_date("Sales for past three months"),
                          [((date.today() - timedelta(days=3 * 30)).replace(day=1)).strftime("%Y-%m-%d"),
                           (date.today() - timedelta(days=date.today().day)).strftime("%Y-%m-%d")])

        self.assertEquals(dt_parse.parse_date("show me sales from 15th November to 6th December"),
                          [date(date.today().year, 11, 15).strftime('%Y-%m-%d'),
                           date(date.today().year, 12, 6).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("show me last two years data"),
                          [date(date.today().year-2, date.today().month, date.today().day).strftime('%Y-%m-%d'),
                           date(date.today().year, date.today().month, date.today().day).strftime('%Y-%m-%d')])

        start_date = date.today() - timedelta(days=date.today().weekday()) - timedelta(days=14)
        end_date = start_date + timedelta(days=7)
        self.assertEquals(dt_parse.parse_date("what was the profit margin previous week"),
                          [start_date.strftime("%Y-%m-%d"),
                           end_date.strftime("%Y-%m-%d")])

        self.assertEquals(dt_parse.parse_date("june 2017 sales information"),
                          [date(2017, 6, 1).strftime('%Y-%m-%d')])


        self.assertEquals(dt_parse.parse_date("show me last month sales"),
                          [(date.today().replace(day=1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d'),
                (date.today().replace(day=1) - timedelta(days=1)).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("show me sales in postal code 300 for the current month"),
                          [date(date.today().year, date.today().month, 1).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("show me last two years sales"),
                          [date(date.today().year - 2, date.today().month, date.today().day).strftime('%Y-%m-%d'),
                           date.today().strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("Show me sales in postal code 2017"),
                          None)

        self.assertEquals(dt_parse.parse_date("Show me sales in 2013"),
                          [date(2013,1,1).strftime('%Y-%m-%d'),
                           date(2013, 12, 31).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("Show me sales between 2013 and 2017"),
                          [date(2013,1,1).strftime('%Y-%m-%d'), date(2017,12,31).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("sales before january 3rd 2013"), ['1970-1-1', '2013-01-03'])

        self.assertEquals(dt_parse.parse_date("sales after 4 july"),
                          [date(date.today().year, 7, 4).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("sales before 30/10"), ['1970-1-1', date(date.today().year, 10, 30).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("sales after 2013/10"), ['2013-01-01', date.today().strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("sales after 12/12/2012"), ['2012-12-12', date.today().strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("Sales this year"),
                          [date(date.today().year, 1, 1).strftime('%Y-%m-%d'),
                           date(date.today().year, date.today().month, date.today().day).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("sales for august"),
                          [date(date.today().year, 8, 1).strftime('%Y-%m-%d'), date(date.today().year, 8, 31).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("sales upto december 8"),
                          ['1970-1-1', date(date.today().year, 12, 8).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("sales for this month"),
                          [date(date.today().year, date.today().month, 1).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("sales for this august"),
                          [date(date.today().year, 8, 1).strftime('%Y-%m-%d'), date(date.today().year, 8, 31).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("Sales on the 14th of January"),
                          [date(date.today().year, 1, 14).strftime('%Y-%m-%d')])

        self.assertEquals(dt_parse.parse_date("Sales in the month of February"),
                          ['2018-02-01', '2018-02-28'])

