from .models import Card
from django.forms.models import model_to_dict
def swap_objects(data):
    try:
        src = Card.objects.get(id=data["card_id_src"])
        dst = Card.objects.get(id=data["card_id_dst"])
        # swap two objects
        src_dict = model_to_dict(src)
        dst_dict = model_to_dict(dst)
        src.title = dst_dict['title']
        src.attachments = dst_dict['attachments']
        src.due_date = dst_dict["due_date"]
        dst.title = src_dict['title']
        dst.attachments = src_dict['attachments']
        dst.due_date = src_dict["due_date"]
        src.save()
        dst.save()
        return True,"ok"
    except Exception as e:
        return False,e