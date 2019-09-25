import asyncio
import gc as _gc

from .parsers import *
from ..operations.Save import save_file, save_dfs, save_analysis
from ..operations.Folder import create_folder, exist, error_record
from ..operations.Folder import is_full as _is_full
from .getter import getter


async def parse(c, names, sheets, update=False, exception=False, error_cache=False):
    """Main parser of the Spyder that wraps up individual parsing rules.

    It calls the async getter function and pass the html to parser (get_summary() etc.),
    and call saver (save_file() etc.) for saving the result in csv format.

    Args:
        c: str - company ticket name, such as AAPL for Apple Inc., only accept ONE ticket.
        names: list - names of ALL sheets, passed in through main().
        sheets: list - sheets that will be saved, passed in through main().
        update: bool - identify if this parse() is used for update(),
            which has different save rules which will be passed to saver (save_file(update=update) etc.).
        exception: bool - print out the exception or not.

    Returns:
        None
    """
    urls = ['https://finance.yahoo.com/quote/{}/holders?p={}'.format(c, c),
            'https://finance.yahoo.com/quote/' + c + '/financials?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/balance-sheet?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/cash-flow?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/key-statistics?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/profile?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '/analysis?p=' + c,
            'https://finance.yahoo.com/quote/' + c + '?p=' + c]

    if isinstance(sheets, str):
        sheets = [sheets]  # double check

    exception_msg = "Exception on {} for {}: {}"
    
    if _is_full(c):
        return
    errors = error_record(activate=error_cache)
    if errors.is_failed(c, 'main'):
        return

    try:

        # Since each individual parser may has different param and save methods,
        # I separated each of them rather than put them into a function.

        create_folder(c)
        if not exist(c, 'Summary', update) and _is_active('Summary', sheets) and not errors.is_failed(c, 'Summary'):
            # update summary
            try:
                html = await getter(urls[7])  # async request
                save_file(get_summary(html, c), c, 'Summary', update)  # save + parse

                del html  # save memory since len(html) is about 500,000
                await asyncio.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'Summary', e)
            except Exception as e:
                if exception:
                    print(exception_msg.format('summary', c, e))
        if not exist(c, names[3:6], update) and _is_active(names[3:6], sheets) and not errors.is_failed(c, 'stats'):
            # update key-statistics
            try:
                html = await getter(urls[4])
                save_dfs(get_stats(html), c, names[3:6])

                del html
                await asyncio.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'stats', e)
            except Exception as e:
                # errors.save_failed(c, 'stats', e)
                if exception:
                    print(exception_msg.format('key-statistics', c, e))
        if not exist(c, names[0:3], update) and _is_active(names[0:3], sheets) and not errors.is_failed(c, 'holders'):
            # update holders
            try:
                html = await getter(urls[0])
                save_file(get_major_holders(html), c, names[0], update)
                save_dfs(get_top_institutional_and_mutual_fund_holders(html), c,
                         [names[1], names[2]])

                del html
                await asyncio.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'holders', e)
            except Exception as e:
                # errors.save_failed(c, 'holders', e)
                if exception:
                    print(exception_msg.format('holders', c, e))
        if not exist(c, names[6:8], update) and _is_active(names[6:8], sheets) and not errors.is_failed(c, 'profile'):
            # update profile
            try:
                html = await getter(urls[5])
                save_dfs([get_executives(html), get_description(html)], c, names[6:8])

                del html
                await asyncio.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'profile', e)
            except Exception as e:
                # errors.save_failed(c, 'profile', e)
                if exception:
                    print(exception_msg.format('profile', c, e))
        if not exist(c, names[8:14], update) and _is_active(names[8:14], sheets) and not errors.is_failed(c, 'analysis'):
            # update analysis
            try:
                html = await getter(urls[6])
                # save_analysis(get_analysis(html), c)
                save_dfs(get_analysis(html), c, names[8:14])

                del html
                await asyncio.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'analysis', e)
            except Exception as e:
                # errors.save_failed(c, 'analysis', e)
                if exception:
                    print(exception_msg.format('analysis', c, e))
        if not exist(c, 'income', update) and _is_active('income', sheets) and not errors.is_failed(c, 'income'):
            # update income
            try:
                html = await getter(urls[1])
                save_file(get_reports(html), c, 'income', update)

                del html
                await asyncio.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'income', e)
            except Exception as e:
                # errors.save_failed(c, 'income', e)
                if exception:
                    print(exception_msg.format('income', c, e))
        if not exist(c, 'balance', update) and _is_active('balance', sheets) and not errors.is_failed(c, 'balance'):
            # update balance
            try:
                html = await getter(urls[2])
                save_file(get_reports(html), c, 'balance', update)

                del html
                await asyncio.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'balance', e)
            except Exception as e:
                # errors.save_failed(c, 'balance', e)
                if exception:
                    print(exception_msg.format('balance-sheet', c, e))
        if not exist(c, 'cash_flow', update) and _is_active('balance', sheets) and not errors.is_failed(c, 'cash_flow'):
            # update cash-flow
            try:
                html = await getter(urls[3])
                save_file(get_reports(html), c, 'cash_flow', update)

                del html
                await asyncio.sleep(0.27)
            except (ValueError, IndexError, KeyError) as e:
                errors.save_failed(c, 'cash_flow', e)
            except Exception as e:
                # errors.save_failed(c, 'cash_flow', e)
                if exception:
                    print(exception_msg.format('cash-flow', c, e))
        _gc.collect()
    except Exception as e:
        errors.save_failed(c, 'main', e)
        # print("Exception on {}: {}".format(c, e))


def _is_active(names, sheets):
    if isinstance(names, str):
        names = [names]
    return set(names).issubset(set(sheets))  # [] in [] regardless of order
