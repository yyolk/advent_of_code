import calendar


class AdventHTMLCalendar(calendar.HTMLCalendar):
    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (calendar.month_name[themonth], theyear)
        else:
            s = '%s' % calendar.month_name[themonth]
        return '<tr><th colspan="7" class="%s">%s</th></tr>' % (self.cssclass_month_head, s)

    def monthdays2calendar(self, year: int, month: int) -> list[list[int]]:
        """Return days of week, 5 at a time."""
        days = list(self.itermonthdays2(year, month))
        return [ days[i:i+5] for i in range(0, len(days), 5)]

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        # a('\n')
        # a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            # Ensure we stop after the last day of the Advent of Code
            if any(filter(lambda x: x[0] > 25, week)):
                break
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
