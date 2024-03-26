package controllers

import javax.inject._
import play.api._
import play.api.mvc._
import play.api.libs.json._

case class Product(id: Long, name: String, price: Double)

object Product {
  implicit val productFormat = Json.format[Product]
}

@Singleton
class ProductController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {
  var products = collection.mutable.ListBuffer(
    Product(1, "Product 1", 10.99),
    Product(2, "Product 2", 19.99),
    Product(3, "Product 3", 5.99)
  )

  def getAllProducts() = Action {
    Ok(Json.toJson(products))
  }

  def getProductById(id: Long) = Action {
    products.find(_.id == id) match {
      case Some(product) => Ok(Json.toJson(product))
      case None => NotFound
    }
  }

  def addProduct() = Action(parse.json) { request =>
    request.body.validate[Product].map { product =>
      products += product
      Created
    }.getOrElse(BadRequest("Invalid product format"))
  }

  def updateProduct(id: Long) = Action(parse.json) { request =>
    request.body.validate[Product].map { updatedProduct =>
      products.find(_.id == id) match {
        case Some(_) =>
          products = products.filterNot(_.id == id)
          products += updatedProduct.copy(id = id)
          Ok(Json.toJson(updatedProduct))
        case None => NotFound
      }
    }.getOrElse(BadRequest("Invalid product format"))
  }

  def deleteProduct(id: Long) = Action {
    products.find(_.id == id) match {
      case Some(_) =>
        products = products.filterNot(_.id == id)
        NoContent
      case None => NotFound
    }
  }
  private def getNextId: Long = {
    if (products.isEmpty) 1
    else products.map(_.id).max + 1
  }
}
