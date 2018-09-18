import asyncio
#存放Puppeteer常见的组合操作

#选取指定path下面所有的img
async def get_all_imgs(page, path):
    rs_list = []
    els = await page.querySelectorAll(path + " img")
    if(els is None):
        return rs_list
    for el in els:
        rs_list.append(await get_element_attr(page, el, "src"))
    return rs_list

#公用操作区

#阻止加载图片
async def _not_loading_images(request):
    if(request.resourceType == "image"):
        await request.abort()
    else:
        await request.continue_()
    
#直接PuppeteerCombo.set_no_image(page)
#阻止加载图片
async def set_no_image(page):
    await page.setRequestInterception(True)
    page.on('request', lambda request: asyncio.ensure_future(_not_loading_images(request)))
    
#基础操作区
async def get_elements_attr_by_selector(page, selector, attr):
    ret_list = []
    elements = await page.querySelectorAll(selector)
    for el in elements:
        tmp_rs = await get_element_attr(page, el, attr)
        if(not tmp_rs is None):
            ret_list.append(tmp_rs)
    return ret_list

async def get_element_attr_by_selector(page, selector, attr):
    element = await page.querySelector(selector)
    return await get_element_attr(page, element, attr)

async def get_element_attr(page, element, attr):    
    if(element is None):
        return None
    data = await page.evaluate('(element) => element.' + attr, element)
    return data
    
async def get_element_content_by_selector(page, selector, need_strip = True):
    check_exist = await check_is_element_exist(page, selector)
    if(not check_exist):
        return ""
    element = await page.querySelector(selector)
    content = await page.evaluate('(element) => element.textContent', element)
    if(need_strip):
        content = content.strip()
    return content
    
async def check_is_element_exist(page, selector):
    el = await page.querySelector(selector);
    if(el is None):
        return False
    else:
        return True
    