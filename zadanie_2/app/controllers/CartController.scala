package controllers

import javax.inject._
import play.api._
import play.api.mvc._
import play.api.libs.json._

case class CartItem(id: Long, productId: Long, quantity: Int)

object CartItem {
  implicit val cartItemFormat = Json.format[CartItem]
}

@Singleton
class CartController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {
  var cartItems = collection.mutable.ListBuffer(
    CartItem(1, 1, 2),
    CartItem(2, 2, 1),
    CartItem(3, 3, 3)
  )

  def getAllCartItems() = Action {
    Ok(Json.toJson(cartItems))
  }

  def getCartItemById(id: Long) = Action {
    cartItems.find(_.id == id) match {
      case Some(cartItem) => Ok(Json.toJson(cartItem))
      case None => NotFound
    }
  }

  def addCartItem() = Action(parse.json) { request =>
    request.body.validate[CartItem].map { cartItem =>
      cartItems += cartItem.copy(id = getNextId)
      Created
    }.getOrElse(BadRequest("Invalid cart item format"))
  }

  def updateCartItem(id: Long) = Action(parse.json) { request =>
    request.body.validate[CartItem].map { updatedCartItem =>
      cartItems.find(_.id == id) match {
        case Some(_) =>
          cartItems = cartItems.filterNot(_.id == id)
          cartItems += updatedCartItem.copy(id = id)
          Ok(Json.toJson(updatedCartItem))
        case None => NotFound
      }
    }.getOrElse(BadRequest("Invalid cart item format"))
  }

  def deleteCartItem(id: Long) = Action {
    cartItems.find(_.id == id) match {
      case Some(_) =>
        cartItems = cartItems.filterNot(_.id == id)
        NoContent
      case None => NotFound
    }
  }

  private def getNextId: Long = {
    if (cartItems.isEmpty) 1
    else cartItems.map(_.id).max + 1
  }
}
