package main

import (
	"net/http"
	"strconv"

	"github.com/labstack/echo/v4"
)

type Product struct {
	ID    int    `json:"id"`
	Name string `json:"name"`
	Price  int    `json:"price"`
}

var products = map[int]*Product{}

var autoIncrementID = 0

func errorHandler(err error, c echo.Context) error {
	code := http.StatusInternalServerError
	if he, ok := err.(*echo.HTTPError); ok {
		code = he.Code
	}
	return c.JSON(code, map[string]string{"error": err.Error()})
}

func createProduct(c echo.Context) error {
	product := new(Product)
	if err := c.Bind(product); err != nil {
		return errorHandler(err, c)
	}
	autoIncrementID++
	product.ID = autoIncrementID
	products[product.ID] = product
	return c.JSON(http.StatusCreated, product)
}

func getAllProducts(c echo.Context) error {
	return c.JSON(http.StatusOK, products)
}

func getProduct(c echo.Context) error {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		return errorHandler(err, c)
	}
	product, ok := products[id]
	if !ok {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "Produkt nie znaleziony"})
	}
	return c.JSON(http.StatusOK, product)
}

func updateProduct(c echo.Context) error {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		return errorHandler(err, c)
	}
	product, ok := products[id]
	if !ok {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "Produkt nie znaleziony"})
	}
	updatedProduct := new(Product)
	if err := c.Bind(updatedProduct); err != nil {
		return errorHandler(err, c)
	}
	product.Name = updatedProduct.Name
	product.Price = updatedProduct.Price
	return c.JSON(http.StatusOK, product)
}

func deleteProduct(c echo.Context) error {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		return errorHandler(err, c)
	}
	delete(products, id)
	return c.NoContent(http.StatusNoContent)
}

func deleteAll(c echo.Context) error {
	products = make(map[int]*Product)
	return c.NoContent(http.StatusNoContent)
}

func main() {
	e := echo.New()

	e.POST("/products", createProduct)
	e.GET("/products", getAllProducts)
	e.GET("/products/:id", getProduct)
	e.PUT("/products/:id", updateProduct)
	e.DELETE("/products/:id", deleteProduct)
	e.DELETE("/products", deleteAll)

	e.Logger.Fatal(e.Start(":8080"))
}
