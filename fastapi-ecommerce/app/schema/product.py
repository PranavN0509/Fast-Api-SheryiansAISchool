from pydantic import BaseModel, Field, AnyUrl, field_validator, model_validator, computed_field
from typing import Annotated, Literal, Optional, List
from uuid import UUID
from datetime import datetime

# IMPORTANT BY deafult when we give examples it uses the first example value in the example value shown on  /docs

class Product(BaseModel):
    id: UUID
    sku: Annotated[
        str, 
        Field(
            min_length=6, 
            max_length=30, 
            title="SKU",
            description="Stock Keeping Unit",
            examples=["734-hjd-378-3d8", "asdasd-asd-sad-"],
        ),
    ]
    name: Annotated[
        str, 
        Field(
            min_length=3, 
            max_length=80, 
            title="Product Name",
            description="Readable Product Name (3-80 chars)",
            examples=["Xiaomi Model Pro", "Apple Model X"],
        ),
    ]
    description: Annotated[
        str,
        Field(
            max_length=200, 
            description="Short product description",
            examples=["This is a short description"]
        )
    ]
    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="Category like mobiles/laptops/electronics/accessories",
            examples=["mobiles", "laptops"]
        ),
    ]
    brand: Annotated[
        str,
        Field(
            min_length=2,
            max_length=40,
            examples=["Xiaomi", "Apple", "Samsung"]
        ),
    ]
    price: Annotated[
        float,
        Field(
            gt=0,
            strict=True,
            description="Base price",
            examples=[20000, 25000]
        )
    ]
    currency: Literal["INR"] = "INR"
    discount_percent: Annotated[
        int,
        Field(
            ge=0, 
            le=90,
            description="Discount in percent (0-90)",
            examples=[10, 15, 18]
        ),
    ] 
    stock: Annotated[
        int,
        Field(
            ge=0, 
            description="Available stock (>=0)",
            examples=[100, 200, 300]
        )
    ]
    is_active: Annotated[
        bool,
        Field(
            description="Is product active",
            examples=[False, True]
        )
    ]
    rating: Annotated[
        float,
        Field(
            ge=0,
            le=5,
            strict=True,
            description="Rating out of 5",
            examples=[3.9, 4.0, 4.5]
        )
    ]
    tags: Annotated[
        Optional[List[str]],
        Field(
            default=None,
            max_length=10,
            description="Up to 10 tags",
            examples=["best-seller, customers-choice"]
        )
    ]
    image_urls: Annotated[
        List[AnyUrl],
        Field(
            default=None,
            max_length=1,
            description="Atleast 1 image url",
            examples=["https://example1.com/", "https://example2.com/"]
        )
    ]
    # dimensions_cm: 
    created_at: datetime

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value:str):
        if "-" not in value:
            raise ValueError("SKU must have '-")    
        last = value.split("-")[-1]
        if not (len(last)==3 and last.isdigit()):
            raise ValueError("SKU must end with a 3-digit sequence like -234")

        return value
    

    @model_validator(mode="after")
    def validate_business_rules(cls, model: "Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stock is 0, is_active must be false")
        
        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted product must have a rating (rating!=0)")
          
        return model
    
    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price* (1-self.discount_percent)/100, 2)