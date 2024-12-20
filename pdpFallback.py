import threading
import time
from pdpIop import get_catalog_ids
from taxonomyCid2Pid import get_hero_products
from taxonomyHandler import fetch_product_details

def pdpFallback(product):
    try:
        pdpRecos = get_catalog_ids(product["catalog_id"])
        pdpRecosWithPid = get_hero_products(pdpRecos)
        product_id_list = [pdpRecosWithPid[cid]  for cid in pdpRecosWithPid]
        product_list = [product["product_id"]] + product_id_list[:]
        productsWithMetaData = fetch_product_details(product_list)
        return {product["product_id"]:productsWithMetaData}
    except Exception as e:
        print(e)
        return {product["product_id"]:[product]}

def pdpFallbackThread(product_list):
    threads = []
    results = []
    for product in product_list:
        thread = threading.Thread(target=lambda pid: results.append(pdpFallback(pid)), args=(product,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    response = {}
    for each_product_resp in results:
        for key in each_product_resp:
            response[key] = each_product_resp[key]
    return response


if __name__=="__main__":
    products = [
        {'product_id': 414147213, 'catalog_id': 122036012, 'sscat_id': 1007, 'sscat_name': 'Blouses', 'widget_metadata': {'image': 'https://images.meesho.com/images/products/414147213/zxu3n.jpg', 'price': None, 'rating': None, 'title': 'Blouses'}},
        {'product_id': 377791243, 'catalog_id': 109874750, 'sscat_id': 1093, 'sscat_name': 'Jewellery Set', 'widget_metadata': {'image': 'https://images.meesho.com/images/products/377791243/mfihx.jpg', 'price': None, 'rating': None, 'title': 'Jewellery Set'}},
        {'product_id': 371223663, 'catalog_id': 107869334, 'sscat_id': 1094, 'sscat_name': 'Bangles & Bracelets', 'widget_metadata': {'image': 'https://images.meesho.com/images/products/371223663/kk3lj.jpg', 'price': None, 'rating': None, 'title': 'Bangles & Bracelets'}},
        {'product_id': 49978414, 'catalog_id': 12492728, 'sscat_id': 1091, 'sscat_name': 'Earrings & Studs', 'widget_metadata': {'image': 'https://images.meesho.com/images/products/49978414/s6yfx.jpg', 'price': None, 'rating': None, 'title': 'Earrings & Studs'}}]
    pdpRecommendations = pdpFallbackThread(products)
    print(pdpRecommendations)
    for each_widget in products:
        print(each_widget)
        print(pdpRecommendations[each_widget["product_id"]])
    # print(pdpRecommendations)
