package controllers

import javax.inject._
import play.api._
import play.api.mvc._
import play.api.libs.json._

case class Category(id: Long, name: String)

object Category {
  implicit val categoryFormat = Json.format[Category]
}

@Singleton
class CategoryController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {
  var categories = collection.mutable.ListBuffer(
    Category(1, "Category 1"),
    Category(2, "Category 2"),
    Category(3, "Category 3")
  )

  def getAllCategories() = Action {
    Ok(Json.toJson(categories))
  }

  def getCategoryById(id: Long) = Action {
    categories.find(_.id == id) match {
      case Some(category) => Ok(Json.toJson(category))
      case None => NotFound
    }
  }

  def addCategory() = Action(parse.json) { request =>
    request.body.validate[Category].map { category =>
      categories += category.copy(id = getNextId)
      Created
    }.getOrElse(BadRequest("Invalid category format"))
  }

  def updateCategory(id: Long) = Action(parse.json) { request =>
    request.body.validate[Category].map { updatedCategory =>
      categories.find(_.id == id) match {
        case Some(_) =>
          categories = categories.filterNot(_.id == id)
          categories += updatedCategory.copy(id = id)
          Ok(Json.toJson(updatedCategory))
        case None => NotFound
      }
    }.getOrElse(BadRequest("Invalid category format"))
  }

  def deleteCategory(id: Long) = Action {
    categories.find(_.id == id) match {
      case Some(_) =>
        categories = categories.filterNot(_.id == id)
        NoContent
      case None => NotFound
    }
  }

  private def getNextId: Long = {
    if (categories.isEmpty) 1
    else categories.map(_.id).max + 1
  }
}
